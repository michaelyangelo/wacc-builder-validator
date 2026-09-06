#!/usr/bin/env python3
"""Solve a simple deterministic reverse-DCF discount rate.

The script is deliberately narrow: it solves enterprise value from FCFF or
equity value from FCFE, with an optional Gordon-growth terminal value. It does
not fetch market data or infer whether a provider's FCF is FCFF.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


class InputError(ValueError):
    """Raised when the reverse-DCF inputs are unsafe or incomplete."""


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise InputError(f"{label} must be finite")
    return result


def _cash_flows(raw: Any) -> list[tuple[float, float]]:
    if not isinstance(raw, list) or not raw:
        raise InputError("cash_flows must be a non-empty list")

    result: list[tuple[float, float]] = []
    for index, item in enumerate(raw, start=1):
        if isinstance(item, dict):
            period = _number(item.get("period", index), f"cash_flows[{index}].period")
            amount = _number(item.get("amount"), f"cash_flows[{index}].amount")
        else:
            period = float(index)
            amount = _number(item, f"cash_flows[{index}]")
        if period <= 0:
            raise InputError("cash-flow periods must be positive")
        result.append((period, amount))

    periods = [period for period, _ in result]
    if periods != sorted(periods) or len(set(periods)) != len(periods):
        raise InputError("cash-flow periods must be unique and ascending")
    return result


def _cash_flow_type(value: Any) -> str:
    if not isinstance(value, str):
        raise InputError("cash_flow_type is required")
    normalized = value.strip().lower()
    aliases = {"fcff": "fcff", "fcfe": "fcfe"}
    if normalized not in aliases:
        raise InputError("cash_flow_type must be FCFF or FCFE")
    return aliases[normalized]


def _validate_basis(value_basis: Any, cash_flow_type: str) -> str:
    if not isinstance(value_basis, str):
        raise InputError("value_basis is required")
    basis = value_basis.strip().lower()
    if basis not in {"enterprise", "equity"}:
        raise InputError("value_basis must be enterprise or equity")
    expected = "fcff" if basis == "enterprise" else "fcfe"
    if cash_flow_type != expected:
        raise InputError(
            f"basis mismatch: {basis} value requires {expected.upper()}, "
            f"not {cash_flow_type.upper()}"
        )
    return basis


def _timing(value: Any) -> str:
    normalized = str(value or "end").strip().lower().replace("-", "_")
    if normalized not in {"end", "mid_year"}:
        raise InputError("timing must be end or mid_year")
    return normalized


def _present_value(
    rate: float,
    cash_flows: list[tuple[float, float]],
    terminal_cash_flow_next_year: float | None,
    terminal_growth: float | None,
    timing: str,
) -> tuple[float, float, float]:
    if rate <= -1:
        return math.inf, math.inf, math.inf
    explicit = 0.0
    for period, amount in cash_flows:
        time = period - 0.5 if timing == "mid_year" else period
        explicit += amount / ((1.0 + rate) ** time)

    terminal = 0.0
    if terminal_cash_flow_next_year is not None:
        if terminal_growth is None:
            raise InputError("terminal_growth is required with terminal_cash_flow_next_year")
        if rate <= terminal_growth:
            return math.inf, explicit, math.inf
        last_period = cash_flows[-1][0]
        terminal_value = terminal_cash_flow_next_year / (rate - terminal_growth)
        terminal_time = last_period
        terminal = terminal_value / ((1.0 + rate) ** terminal_time)
    return explicit + terminal, explicit, terminal


def _validate_cash_flow_pattern(
    cash_flows: list[tuple[float, float]], terminal_cash_flow: float | None
) -> None:
    """Support one negative-to-positive sign change, including -value at t=0.

    Leading forecast losses are supported. A later negative cash flow after
    positive receipts, or a negative perpetuity, is outside this solver's
    uniqueness guarantee and must not return an apparently unique rate.
    """
    positive_seen = False
    for amount in [amount for _, amount in cash_flows] + (
        [terminal_cash_flow] if terminal_cash_flow is not None else []
    ):
        if amount < 0 and positive_seen:
            raise InputError("unsupported cash-flow sign pattern: multiple rates may exist")
        if amount > 0:
            positive_seen = True
    if terminal_cash_flow is not None and terminal_cash_flow < 0:
        raise InputError("negative terminal cash flow is outside the supported solver domain")
    if not positive_seen:
        raise InputError("positive value requires at least one positive future cash flow")


def _solve(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise InputError("input must be a JSON object")

    cash_flow_type = _cash_flow_type(payload.get("cash_flow_type"))
    basis = _validate_basis(payload.get("value_basis"), cash_flow_type)
    value = _number(payload.get("value"), "value")
    if value <= 0:
        raise InputError("value must be positive")
    cash_flows = _cash_flows(payload.get("cash_flows"))
    timing = _timing(payload.get("timing"))
    if timing == "mid_year" and cash_flows[0][0] <= 0.5:
        raise InputError("mid_year requires all cash-flow periods to exceed 0.5")

    if "terminal_cash_flow" in payload:
        raise InputError(
            "ambiguous terminal_cash_flow is no longer accepted; supply "
            "terminal_cash_flow_next_year, already grown to period n+1"
        )
    terminal_cash_flow = payload.get("terminal_cash_flow_next_year")
    if terminal_cash_flow is not None:
        terminal_cash_flow = _number(terminal_cash_flow, "terminal_cash_flow_next_year")
    terminal_growth = payload.get("terminal_growth")
    if terminal_growth is not None:
        terminal_growth = _number(terminal_growth, "terminal_growth")
        if terminal_growth <= -1:
            raise InputError("terminal_growth must exceed -100%")
    if terminal_cash_flow is not None and terminal_growth is None:
        raise InputError("terminal_growth is required with terminal_cash_flow_next_year")
    if terminal_growth is not None and terminal_cash_flow is None:
        raise InputError("terminal_cash_flow_next_year is required with terminal_growth")
    _validate_cash_flow_pattern(cash_flows, terminal_cash_flow)

    default_lower = max(0.0, terminal_growth + 1e-6) if terminal_growth is not None else 0.0
    bracket = payload.get("rate_bracket", [default_lower, max(1.0, default_lower + 1.0)])
    if not isinstance(bracket, list) or len(bracket) != 2:
        raise InputError("rate_bracket must contain [minimum, maximum]")
    lower = _number(bracket[0], "rate_bracket[0]")
    upper = _number(bracket[1], "rate_bracket[1]")
    if upper <= lower:
        raise InputError("rate_bracket maximum must exceed minimum")
    if lower <= -1:
        raise InputError("rate_bracket minimum must exceed -100%")
    if terminal_growth is not None and lower <= terminal_growth:
        raise InputError("rate_bracket minimum must exceed terminal_growth")

    def residual(rate: float) -> float:
        try:
            present_value, _, _ = _present_value(
                rate, cash_flows, terminal_cash_flow, terminal_growth, timing
            )
        except (OverflowError, ZeroDivisionError) as exc:
            raise InputError("nonfinite present value; use a narrower rate_bracket") from exc
        result = present_value - value
        if not math.isfinite(result):
            raise InputError("nonfinite present value; use a narrower rate_bracket")
        return result

    left, right = lower, upper
    left_residual, right_residual = residual(left), residual(right)
    tolerance = max(1e-11, abs(value) * 1e-12)
    if abs(left_residual) <= tolerance:
        solved = left
    elif abs(right_residual) <= tolerance:
        solved = right
    elif (left_residual > 0) == (right_residual > 0):
        raise InputError("no rate in rate_bracket; supply a justified wider bracket")
    else:
        for _ in range(200):
            middle = (left + right) / 2.0
            middle_residual = residual(middle)
            if abs(middle_residual) <= tolerance:
                solved = middle
                break
            if (left_residual > 0) != (middle_residual > 0):
                right = middle
            else:
                left = middle
                left_residual = middle_residual
        else:
            solved = (left + right) / 2.0

    present_value, explicit_pv, terminal_pv = _present_value(
        solved, cash_flows, terminal_cash_flow, terminal_growth, timing
    )
    if abs(present_value - value) > tolerance:
        raise InputError("solver did not meet the value residual tolerance")
    return {
        "value_basis": basis,
        "cash_flow_type": cash_flow_type.upper(),
        "timing": timing,
        "implied_rate": solved,
        "implied_rate_percent": solved * 100.0,
        "residual": present_value - value,
        "explicit_cash_flow_pv": explicit_pv,
        "terminal_value_pv": terminal_pv,
        "terminal_value_share": terminal_pv / present_value if present_value else None,
        "terminal_growth": terminal_growth,
        "terminal_cash_flow_next_year": terminal_cash_flow,
        "terminal_timing": "end_of_final_explicit_period",
        "rate_bracket": [lower, upper],
        "uniqueness_basis": "single_negative_to_positive_cash_flow_sign_change",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON file path or - for stdin")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    try:
        raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        result = _solve(json.loads(raw))
    except (OSError, json.JSONDecodeError, InputError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

