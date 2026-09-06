#!/usr/bin/env python3
"""Deterministic peer-beta regression, normalization, and relevering."""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any


class InputError(ValueError):
    """Raised when peer-beta inputs are invalid."""


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{label} is required")
    return value.strip()


def _date(value: Any, label: str) -> date:
    text = _text(value, label)
    try:
        result = date.fromisoformat(text)
    except ValueError as exc:
        raise InputError(f"{label} must be an ISO date (YYYY-MM-DD)") from exc
    if result.isoformat() != text:
        raise InputError(f"{label} must be an ISO date (YYYY-MM-DD)")
    return result


def _period_indices(dates: list[date], frequency: str, valuation_date: date) -> list[int]:
    if len(dates) < 2 or dates != sorted(set(dates)):
        raise InputError("observation dates must be unique and ascending")
    if dates[-1] > valuation_date:
        raise InputError("observation date is after valuation_date")
    if frequency == "five_year_monthly":
        periods = [item.year * 12 + item.month for item in dates]
        if periods[-1] - periods[0] != 60:
            raise InputError("five_year_monthly must span 60 calendar months")
        if (valuation_date - dates[-1]).days > 35:
            raise InputError("monthly window must end at the valuation-date period")
    else:
        periods = [(item.toordinal() - item.weekday()) // 7 for item in dates]
        if not 103 <= periods[-1] - periods[0] <= 105:
            raise InputError("two_year_weekly must span approximately two years (103-105 weeks)")
        if (valuation_date - dates[-1]).days > 10:
            raise InputError("weekly window must end at the valuation-date period")
    if len(periods) != len(set(periods)):
        raise InputError("multiple observations in one claimed monthly/weekly period")
    return periods


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise InputError(f"{label} must be finite")
    return result


def _positive(value: Any, label: str) -> float:
    result = _number(value, label)
    if result <= 0:
        raise InputError(f"{label} must be positive")
    return result


def _returns(levels: list[Any], label: str) -> list[float]:
    if len(levels) < 3:
        raise InputError(f"{label} needs at least three price levels")
    values = [_positive(value, f"{label}[{index}]") for index, value in enumerate(levels)]
    return [values[index] / values[index - 1] - 1.0 for index in range(1, len(values))]


def _regression(
    stock_returns: list[float], market_returns: list[float]
) -> dict[str, float | int | None]:
    if len(stock_returns) != len(market_returns):
        raise InputError("stock and market returns must have the same length")
    if len(stock_returns) < 2:
        raise InputError("at least two aligned returns are required")

    count = len(stock_returns)
    mean_stock = sum(stock_returns) / count
    mean_market = sum(market_returns) / count
    market_ss = sum((value - mean_market) ** 2 for value in market_returns)
    if market_ss == 0:
        raise InputError("market returns have zero variance")

    covariance_sum = sum(
        (stock - mean_stock) * (market - mean_market)
        for stock, market in zip(stock_returns, market_returns)
    )
    beta = covariance_sum / market_ss
    alpha = mean_stock - beta * mean_market
    fitted = [alpha + beta * market for market in market_returns]
    residual_ss = sum((stock - estimate) ** 2 for stock, estimate in zip(stock_returns, fitted))
    stock_ss = sum((stock - mean_stock) ** 2 for stock in stock_returns)
    r_squared = 0.0 if stock_ss == 0 else 1.0 - residual_ss / stock_ss
    standard_error: float | None = None
    if count > 2:
        residual_variance = residual_ss / (count - 2)
        standard_error = math.sqrt(residual_variance / market_ss)

    beta_t_stat = None
    if standard_error not in {None, 0.0}:
        beta_t_stat = beta / standard_error

    return {
        "observations": count,
        "alpha": alpha,
        "levered_beta": beta,
        "r_squared": r_squared,
        "beta_standard_error": standard_error,
        "beta_t_stat": beta_t_stat,
    }


def _unlever(beta: float, debt: float, equity: float, tax_rate: float) -> float:
    if equity <= 0:
        raise InputError("peer equity must be positive")
    if debt < 0:
        raise InputError("peer debt cannot be negative")
    if not 0 <= tax_rate < 1:
        raise InputError("tax rate must be between 0 and 1")
    return beta / (1.0 + (1.0 - tax_rate) * debt / equity)


def _relever(beta: float, debt: float, equity: float, tax_rate: float) -> float:
    if equity <= 0:
        raise InputError("target equity must be positive")
    if debt < 0:
        raise InputError("target debt cannot be negative")
    if not 0 <= tax_rate < 1:
        raise InputError("target tax rate must be between 0 and 1")
    return beta * (1.0 + (1.0 - tax_rate) * debt / equity)


def _weighted_mean(values: list[float], weights: list[float]) -> float:
    total = sum(weights)
    if total <= 0:
        raise InputError("peer weights must sum to a positive value")
    return sum(value * weight for value, weight in zip(values, weights)) / total


def _median(values: list[float]) -> float:
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / 2.0


def assess(payload: dict[str, Any]) -> dict[str, Any]:
    """Calculate peer regressions and a beta on the target ERP basis."""

    if not isinstance(payload, dict):
        raise InputError("input must be an object")
    peers = payload.get("peers")
    if not isinstance(peers, list) or not peers:
        raise InputError("peers must be a non-empty list")

    target_erp = _positive(payload.get("target_erp"), "target_erp")
    target_benchmark = _text(payload.get("target_benchmark"), "target_benchmark")
    target_erp_market = _text(payload.get("target_erp_market"), "target_erp_market")
    target_currency = _text(payload.get("target_return_currency"), "target_return_currency")
    valuation_date = _date(payload.get("valuation_date"), "valuation_date")
    target = payload.get("target")
    if not isinstance(target, dict):
        raise InputError("target must be an object")

    results: list[dict[str, Any]] = []
    risk_contributions: list[float] = []
    unlevered_target_betas: list[float] = []
    weights: list[float] = []

    for index, peer in enumerate(peers):
        if not isinstance(peer, dict):
            raise InputError(f"peers[{index}] must be an object")
        name = str(peer.get("name") or f"peer_{index + 1}")
        source_erp = _positive(peer.get("source_erp"), f"{name}.source_erp")
        weight = _positive(peer.get("weight", 1.0), f"{name}.weight")
        metadata = {key: _text(peer.get(key), f"{name}.{key}") for key in (
            "benchmark", "return_currency", "erp_market", "source"
        )}

        regression: dict[str, float | int | None] | None = None
        if "observations" in peer:
            observations = peer["observations"]
            if not isinstance(observations, list):
                raise InputError(f"{name}.observations must be a list")
            frequency = peer.get("frequency")
            if frequency not in ("five_year_monthly", "two_year_weekly"):
                raise InputError(
                    f"{name}.frequency must be five_year_monthly or two_year_weekly"
                )
            price_type = peer.get("price_type")
            if price_type not in ("adjusted_close", "total_return"):
                raise InputError(
                    f"{name}.price_type must be adjusted_close or total_return"
                )
            if metadata["return_currency"].upper() != target_currency.upper():
                raise InputError(f"{name}: convert return series to target_return_currency first")
            if metadata["benchmark"].casefold() != target_benchmark.casefold():
                raise InputError(f"{name}: regression requires the common target_benchmark")
            stock_levels = []
            market_levels = []
            dates = []
            for observation_index, observation in enumerate(observations):
                if not isinstance(observation, dict):
                    raise InputError(f"{name}.observations[{observation_index}] must be an object")
                dates.append(_date(observation.get("date"), f"{name}.observations[{observation_index}].date"))
                stock_levels.append(observation.get("stock"))
                market_levels.append(observation.get("market"))
            periods = _period_indices(dates, frequency, valuation_date)
            stock_returns = _returns(stock_levels, f"{name}.stock")
            market_returns = _returns(market_levels, f"{name}.market")
            # A return spanning a missing period is not a one-period return.
            adjacent = [index for index in range(len(periods)-1)
                        if periods[index+1] - periods[index] == 1]
            regression = _regression([stock_returns[i] for i in adjacent],
                                     [market_returns[i] for i in adjacent])
            minimum_returns_value = _number(
                peer.get("minimum_returns", 60), f"{name}.minimum_returns"
            )
            if minimum_returns_value < 60 or not minimum_returns_value.is_integer():
                raise InputError(f"{name}.minimum_returns must be an integer of at least 60")
            minimum_returns = int(minimum_returns_value)
            if regression["observations"] < minimum_returns:
                raise InputError(
                    f"{name} has {regression['observations']} returns; "
                    f"minimum is {minimum_returns}"
                )
            levered_beta = regression["levered_beta"]
            regression["excluded_gap_returns"] = len(stock_returns) - len(adjacent)
            regression["first_date"] = dates[0].isoformat()
            regression["last_date"] = dates[-1].isoformat()
        else:
            levered_beta = _number(peer.get("levered_beta"), f"{name}.levered_beta")
            for key in ("frequency", "lookback", "beta_adjustment"):
                metadata[key] = _text(peer.get(key), f"{name}.{key}")
            source_date = _date(peer.get("source_date"), f"{name}.source_date")
            if source_date > valuation_date:
                raise InputError(f"{name}.source_date is after valuation_date")
            metadata["source_date"] = source_date.isoformat()

        debt = _number(peer.get("debt"), f"{name}.debt")
        equity = _positive(peer.get("equity"), f"{name}.equity")
        tax_rate = _number(peer.get("tax_rate"), f"{name}.tax_rate")
        unlevered_beta = _unlever(levered_beta, debt, equity, tax_rate)
        risk_contribution = unlevered_beta * source_erp
        target_basis_beta = risk_contribution / target_erp

        result = {
            "name": name,
            "levered_beta": levered_beta,
            "unlevered_beta_source_basis": unlevered_beta,
            "source_erp": source_erp,
            "unlevered_risk_contribution": risk_contribution,
            "unlevered_beta_target_basis": target_basis_beta,
            "weight": weight,
            **metadata,
        }
        if regression is not None:
            result["regression"] = regression
            result["benchmark"] = peer["benchmark"]
            result["return_currency"] = peer["return_currency"]
            result["frequency"] = peer["frequency"]
            result["price_type"] = peer["price_type"]
        results.append(result)
        risk_contributions.append(risk_contribution)
        unlevered_target_betas.append(target_basis_beta)
        weights.append(weight)

    weighted_risk_contribution = _weighted_mean(risk_contributions, weights)
    weighted_unlevered_target_beta = weighted_risk_contribution / target_erp
    median_unlevered_target_beta = _median(unlevered_target_betas)
    target_debt = _number(target.get("debt"), "target.debt")
    target_equity = _positive(target.get("equity"), "target.equity")
    target_tax = _number(target.get("tax_rate"), "target.tax_rate")

    return {
        "target_benchmark": target_benchmark,
        "target_erp_market": target_erp_market,
        "target_return_currency": target_currency,
        "valuation_date": valuation_date.isoformat(),
        "calculation_only": True,
        "source_and_erp_coherence": "requires_evidence_review",
        "cross_benchmark_approximation": any(
            result["benchmark"].casefold() != target_benchmark.casefold()
            or result["erp_market"].casefold() != target_erp_market.casefold()
            for result in results
        ),
        "target_erp": target_erp,
        "peer_results": results,
        "weighted_unlevered_risk_contribution": weighted_risk_contribution,
        "weighted_unlevered_beta_target_basis": weighted_unlevered_target_beta,
        "median_unlevered_beta_target_basis": median_unlevered_target_beta,
        "weighted_relevered_beta_target_basis": _relever(
            weighted_unlevered_target_beta, target_debt, target_equity, target_tax
        ),
        "median_relevered_beta_target_basis": _relever(
            median_unlevered_target_beta, target_debt, target_equity, target_tax
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", nargs="?", help="JSON input payload (legacy positional form)")
    parser.add_argument("--input", help="JSON file path or - for stdin")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    if bool(args.input_path) == bool(args.input):
        parser.error("supply exactly one input file, using --input or the positional form")
    try:
        path = args.input or args.input_path
        raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
        output = json.dumps(assess(json.loads(raw)),
                            indent=2 if args.pretty else None, allow_nan=False)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
