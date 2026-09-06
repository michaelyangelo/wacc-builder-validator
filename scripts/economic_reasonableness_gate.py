#!/usr/bin/env python3
"""Deterministic diagnostics for the discount-rate economic gate."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


class InputError(ValueError):
    """Raised when gate inputs are invalid."""


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise InputError(f"{label} must be finite")
    return result


def _optional_number(payload: dict[str, Any], key: str) -> float | None:
    value = payload.get(key)
    return None if value is None else _number(value, key)


def _terminal_multiples(rate: float, growth: float) -> dict[str, float]:
    if rate <= growth:
        raise InputError("rate must exceed terminal_growth")
    spread = rate - growth
    return {
        "rate_minus_growth": spread,
        "tv_to_next_year_fcff": 1.0 / spread,
        "tv_to_current_year_fcff": (1.0 + growth) / spread,
    }


def _evidence_state(value: Any, label: str) -> str:
    if value is True or value == "supported":
        return "supported"
    if value is False or value == "unsupported":
        return "unsupported"
    if value is None or value == "unknown":
        return "unknown"
    if value == "not_applicable":
        return "not_applicable"
    raise InputError(f"{label} must be supported, unsupported, unknown, or not_applicable")


def assess(payload: dict[str, Any]) -> dict[str, Any]:
    """Assess calculated, selected and applied rates for one application."""

    if not isinstance(payload, dict):
        raise InputError("input must be an object")

    payload = dict(payload)
    control_fields = (
        "conventional_wacc_requested", "professional_wacc_requested", "beta_used",
        "beta_erp_match", "unmatched_scenario_explicitly_requested",
        "market_source_bundle_used", "source_bundle_coherent", "external_market_inputs_used",
        "latest_available_source_vintage_used", "market_security_values_used",
        "security_source_match", "rating_spread_proxy_used", "rating_scale_mapping_supported",
        "new_mechanical_wacc_from_blocked_inputs", "currency_basis_adjustment_supported",
        "country_risk_overlap", "quick_path_explicitly_selected", "beta_range_used",
        "beta_range_basis_supported", "external_reliance_requested", "highest_effort_requested",
        "material_decision", "beta_coherence_problem", "regression_data_available",
        "capital_stack_issue", "basis_mismatch",
    )
    for key in control_fields:
        if payload.get(key) is not None and not isinstance(payload[key], bool):
            raise InputError(f"{key} must be boolean or null")
    if payload.get("beta_path") not in (None, "Q", "P", "R"):
        raise InputError("beta_path must be Q, P, or R")
    rates = {
        "calculated": _number(payload.get("calculated_rate"), "calculated_rate"),
        "selected": _optional_number(payload, "selected_rate"),
        "applied": _optional_number(payload, "applied_rate"),
    }
    for role, value in rates.items():
        if value is not None and value <= -1:
            raise InputError(f"{role}_rate must exceed -100%")
    rate = rates["calculated"]

    diagnostics: dict[str, Any] = {}
    flags: list[str] = []
    hard_blocks: list[str] = []
    missing_evidence: list[str] = []
    evidence_keys = (
        "method_evidence_supported", "cash_flow_evidence_available",
        "application_basis_supported", "debt_cost_policy_match",
        "hybrid_treatment_resolved", "selected_rate_evidence_supported",
        "applied_rate_evidence_supported",
    )
    evidence = {key: _evidence_state(payload.get(key), key) for key in evidence_keys}
    debt_weight = _optional_number(payload, "debt_weight")
    if debt_weight is not None and not 0 <= debt_weight <= 1:
        raise InputError("debt_weight must be between 0 and 1")
    wacc_requested = (
        payload.get("conventional_wacc_requested") is True
        or payload.get("professional_wacc_requested") is True
    )
    for key in evidence_keys:
        if evidence[key] == "not_applicable" and not (
            key == "debt_cost_policy_match" and debt_weight == 0
        ):
            raise InputError(f"{key}: not_applicable is allowed only for zero-weight debt cost")
        payload[key] = {"supported": True, "unsupported": False}.get(evidence[key])
    if debt_weight == 0:
        evidence["debt_cost_policy_match"] = "not_applicable"
        payload["debt_cost_policy_match"] = None
    required = ["method_evidence_supported", "cash_flow_evidence_available",
                "application_basis_supported"]
    if wacc_requested:
        required.append("hybrid_treatment_resolved")
        if debt_weight != 0:
            required.append("debt_cost_policy_match")
    for key in required:
        if evidence[key] == "unknown":
            missing_evidence.append(key)
        elif evidence[key] == "unsupported":
            hard_blocks.append(f"{key}_unsupported")

    region_basis = payload.get("region_basis")
    if region_basis not in (None, "eu_eea", "outside_eu_eea"):
        raise InputError("region_basis must be eu_eea or outside_eu_eea")
    base_rate_anchor = payload.get("base_rate_anchor")
    regional_policy_required = any(
        (
            payload.get("conventional_wacc_requested") is True,
            payload.get("professional_wacc_requested") is True,
            payload.get("beta_used") is True,
            base_rate_anchor is not None,
        )
    )
    if region_basis is None and regional_policy_required:
        hard_blocks.append("regional_base_rate_policy_unresolved")
    elif region_basis == "eu_eea" and base_rate_anchor != "bund":
        hard_blocks.append("eu_eea_base_rate_policy_violation")
    elif (
        region_basis == "outside_eu_eea"
        and base_rate_anchor != "us_treasury"
    ):
        hard_blocks.append("outside_eu_eea_base_rate_policy_violation")

    beta_erp_match = payload.get("beta_erp_match")
    if beta_erp_match is False:
        hard_blocks.append("beta_erp_market_mismatch")
    elif beta_erp_match is None and payload.get("beta_used") is True:
        if payload.get("unmatched_scenario_explicitly_requested") is True:
            flags.append("beta_erp_match_unverified_scenario_only")
        else:
            hard_blocks.append("beta_erp_match_unverified")

    if (
        payload.get("market_source_bundle_used") is True
        and payload.get("source_bundle_coherent") is not True
    ):
        hard_blocks.append("market_source_bundle_incoherent")

    if (
        payload.get("external_market_inputs_used") is True
        and payload.get("latest_available_source_vintage_used") is not True
    ):
        hard_blocks.append("stale_or_unchecked_source_vintage")

    if (
        payload.get("market_security_values_used") is True
        and payload.get("security_source_match") is not True
    ):
        hard_blocks.append("security_source_identity_mismatch")

    if payload.get("debt_cost_policy_match") is False:
        hard_blocks.append("debt_cost_policy_violation")

    if (
        payload.get("rating_spread_proxy_used") is True
        and payload.get("rating_scale_mapping_supported") is not True
    ):
        hard_blocks.append("rating_scale_mapping_unsupported")

    if (
        wacc_requested
        and payload.get("hybrid_treatment_resolved") is False
    ):
        hard_blocks.append("hybrid_claim_unresolved_for_wacc")

    if payload.get("new_mechanical_wacc_from_blocked_inputs") is True:
        hard_blocks.append("invented_mechanical_wacc_from_blocked_inputs")

    cash_flow_currency = payload.get("cash_flow_currency")
    if cash_flow_currency is not None and not isinstance(cash_flow_currency, str):
        raise InputError("cash_flow_currency must be text or null")
    if isinstance(cash_flow_currency, str):
        cash_flow_currency = cash_flow_currency.strip().upper()
    if wacc_requested and not cash_flow_currency:
        missing_evidence.append("cash_flow_currency")
    anchor_currency = {"eu_eea": "EUR", "outside_eu_eea": "USD"}.get(
        region_basis
    )
    if (
        anchor_currency is not None
        and cash_flow_currency not in {None, anchor_currency}
        and payload.get("currency_basis_adjustment_supported") is not True
    ):
        hard_blocks.append("cash_flow_currency_basis_adjustment_missing")

    if payload.get("country_risk_overlap") is True:
        hard_blocks.append("country_risk_double_counting")

    beta_path = payload.get("beta_path")
    if beta_path == "Q":
        flags.append("quick_beta_path_is_provisional")
        if (
            payload.get("professional_wacc_requested") is True
            and payload.get("quick_path_explicitly_selected") is not True
        ):
            hard_blocks.append("quick_path_not_user_selected")
    if (
        payload.get("beta_range_used") is True
        and payload.get("beta_range_basis_supported") is not True
    ):
        hard_blocks.append("beta_range_basis_unsupported")
    path_r_warranted = any(
        (
            payload.get("external_reliance_requested") is True,
            payload.get("highest_effort_requested") is True,
            payload.get("material_decision") is True,
            payload.get("beta_coherence_problem") is True,
            beta_erp_match is False,
        )
    )
    if (
        path_r_warranted
        and payload.get("regression_data_available") is True
        and beta_path != "R"
    ):
        flags.append("regression_multi_verification_not_run")

    risk_free = _optional_number(payload, "risk_free_rate")
    cost_of_equity = _optional_number(payload, "cost_of_equity")
    if risk_free is not None and cost_of_equity is not None:
        diagnostics["equity_premium_implied"] = cost_of_equity - risk_free

    pre_tax_cost_of_debt = _optional_number(payload, "pre_tax_cost_of_debt")
    after_tax_cost_of_debt = _optional_number(payload, "after_tax_cost_of_debt")
    if cost_of_equity is not None and pre_tax_cost_of_debt is not None:
        diagnostics["pre_tax_kd_minus_ke_bps"] = (
            pre_tax_cost_of_debt - cost_of_equity
        ) * 10_000
        if pre_tax_cost_of_debt > cost_of_equity:
            flags.append("pre_tax_debt_cost_above_equity_cost_investigate")
    if cost_of_equity is not None and after_tax_cost_of_debt is not None:
        diagnostics["after_tax_kd_minus_ke_bps"] = (
            after_tax_cost_of_debt - cost_of_equity
        ) * 10_000
        if after_tax_cost_of_debt > cost_of_equity:
            flags.append("after_tax_debt_cost_above_equity_cost_investigate")

    growth = _optional_number(payload, "terminal_growth")
    if growth is not None and growth <= -1:
        raise InputError("terminal_growth must exceed -100%")

    terminal_share = _optional_number(payload, "terminal_value_share")
    if terminal_share is not None:
        diagnostics["terminal_value_share"] = terminal_share
        if terminal_share > 0.75:
            flags.append("high_terminal_value_concentration")
        if terminal_share > 1:
            flags.append("terminal_value_exceeds_total_value_review_negative_explicit_pv")
        elif terminal_share < 0:
            flags.append("negative_terminal_value_share_review_value_basis")

    market_implied = _optional_number(payload, "market_implied_rate")
    if market_implied is not None:
        diagnostics["market_rate_difference_bps"] = (rate - market_implied) * 10_000
        warning_bps = payload.get("market_gap_warning_bps")
        if warning_bps is not None:
            warning_bps = _number(warning_bps, "market_gap_warning_bps")
            if warning_bps < 0:
                raise InputError("market_gap_warning_bps cannot be negative")
            if abs(diagnostics["market_rate_difference_bps"]) > warning_bps:
                flags.append("material_bottom_up_market_rate_gap")
    else:
        flags.append("market_implied_rate_not_testable")

    if payload.get("cash_flow_evidence_available") is not True:
        flags.append("cash_flow_evidence_not_testable")

    if payload.get("capital_stack_issue") is True:
        flags.append("material_capital_stack_issue")

    if payload.get("basis_mismatch") is True:
        hard_blocks.append("cash_flow_value_basis_mismatch")

    # One call covers one claim, cash-flow schedule, currency and timing basis.
    # Keep observed bad rates visible and assess each instead of substituting
    # the mechanical calculation for the user's actual application.
    rate_assessments: dict[str, Any] = {}
    for role, value in rates.items():
        role_blocks = list(hard_blocks)
        role_flags = list(flags)
        role_missing = list(missing_evidence)
        role_diagnostics: dict[str, Any] = {}
        if value is None:
            role_missing.append(f"{role}_rate")
        elif role != "calculated":
            key = f"{role}_rate_evidence_supported"
            if evidence[key] == "unknown":
                role_missing.append(key)
            elif evidence[key] == "unsupported":
                role_blocks.append(f"{role}_rate_evidence_unsupported")
        if value is not None and growth is not None:
            if value <= growth:
                role_blocks.append(f"{role}_rate_not_above_terminal_growth")
            else:
                role_diagnostics["terminal_multiples"] = _terminal_multiples(value, growth)
                if value - growth < 0.02:
                    role_flags.append(f"{role}_narrow_rate_growth_spread")
        role_status = (
            "BLOCKED" if role_blocks else "NOT TESTABLE" if role_missing
            else "CAUTION" if role_flags else "PASS"
        )
        rate_assessments[role] = {
            "rate": value, "status": role_status, "hard_blocks": role_blocks,
            "flags": role_flags, "missing_evidence": role_missing,
            "diagnostics": role_diagnostics,
        }
    diagnostics.update(rate_assessments["calculated"]["diagnostics"])
    hard_blocks = list(dict.fromkeys(
        block for result in rate_assessments.values() for block in result["hard_blocks"]
    ))
    flags = list(dict.fromkeys(
        flag for result in rate_assessments.values() for flag in result["flags"]
    ))
    missing_evidence = list(dict.fromkeys(
        key for result in rate_assessments.values() for key in result["missing_evidence"]
    ))
    if hard_blocks:
        status = "BLOCKED"
    elif missing_evidence:
        status = "NOT TESTABLE"
    elif flags:
        status = "CAUTION"
    else:
        status = "PASS"

    if (
        status in {"BLOCKED", "NOT TESTABLE"}
        or "beta_erp_match_unverified_scenario_only" in flags
        or payload.get("beta_path") == "Q"
    ):
        reliance = "Not ready to rely on"
    elif status == "CAUTION":
        reliance = "Ready with caveats"
    else:
        reliance = "Ready to use"

    return {
        "status": status,
        "reliance_state": reliance,
        "flags": flags,
        "hard_blocks": hard_blocks,
        "diagnostics": diagnostics,
        "missing_evidence": missing_evidence,
        "evidence_states": evidence,
        "rate_assessments": rate_assessments,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON file path or - for stdin")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        result = assess(json.loads(raw))
        output = json.dumps(result, indent=2 if args.pretty else None, allow_nan=False)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

