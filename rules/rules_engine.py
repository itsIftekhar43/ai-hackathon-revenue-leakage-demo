from typing import Dict, List, Any


DEFAULT_THRESHOLDS = {
    "max_refund_pct": 0.8,  # refund greater than 80% of fare is suspicious
    "high_commission_pct": 0.5,  # commission > 50% of fare = high
}


def _make_issue(code: str, message: str, severity: str = "medium", field: str | None = None, value: Any = None) -> Dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "severity": severity,
        "field": field,
        "value": value,
    }


def validate_record(record: Dict[str, Any], thresholds: Dict[str, float] | None = None) -> List[Dict[str, Any]]:
    """Validate a transaction record and return structured issues.

    Returns a list of issue objects:
    {
      'code': 'NEG_TAX', 'message': 'Negative tax detected', 'severity': 'high', 'field': 'tax', 'value': -20
    }

    The function also performs some aggregate checks and flags severity accordingly.
    """
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    issues: List[Dict[str, Any]] = []

    fare = record.get("fare")
    tax = record.get("tax")
    commission = record.get("commission")
    refund = record.get("refund_amount")

    # Basic validations
    if fare is None:
        issues.append(_make_issue("MISSING_FARE", "Missing fare", "high", "fare", fare))
    else:
        try:
            f = float(fare)
            if f <= 0:
                issues.append(_make_issue("INVALID_FARE", "Invalid fare amount", "high", "fare", fare))
        except Exception:
            issues.append(_make_issue("INVALID_FARE_TYPE", "Fare must be numeric", "high", "fare", fare))

    if tax is None:
        issues.append(_make_issue("MISSING_TAX", "Missing tax", "low", "tax", tax))
    else:
        try:
            t = float(tax)
            if t < 0:
                issues.append(_make_issue("NEG_TAX", "Negative tax detected", "high", "tax", tax))
            elif fare is not None and float(fare) > 0 and t > float(fare) * 0.5:
                issues.append(_make_issue("HIGH_TAX", "Tax unusually high relative to fare", "medium", "tax", tax))
        except Exception:
            issues.append(_make_issue("INVALID_TAX_TYPE", "Tax must be numeric", "high", "tax", tax))

    if commission is None:
        issues.append(_make_issue("MISSING_COMMISSION", "Missing commission", "low", "commission", commission))
    else:
        try:
            c = float(commission)
            if c < 0:
                issues.append(_make_issue("NEG_COMMISSION", "Negative commission detected", "high", "commission", commission))
            else:
                if fare is not None and float(fare) >= 0:
                    if c > float(fare):
                        issues.append(_make_issue("COMMISSION_EXCEEDS_FARE", "Commission exceeds fare", "high", "commission", commission))
                    elif c > float(fare) * thresholds.get("high_commission_pct", 0.5):
                        issues.append(_make_issue("HIGH_COMMISSION_RATIO", "Commission unusually large relative to fare", "medium", "commission", commission))
        except Exception:
            issues.append(_make_issue("INVALID_COMMISSION_TYPE", "Commission must be numeric", "high", "commission", commission))

    if refund is None:
        # refunds are optional, don't add missing unless explicitly required
        refund = 0
    else:
        try:
            r = float(refund)
            if r < 0:
                issues.append(_make_issue("NEG_REFUND", "Negative refund amount", "high", "refund_amount", refund))
            if fare is not None and float(fare) >= 0 and r > float(fare):
                issues.append(_make_issue("REFUND_EXCEEDS_FARE", "Refund exceeds fare", "high", "refund_amount", refund))
            if fare is not None and float(fare) > 0 and r > float(fare) * thresholds.get("max_refund_pct", 0.8):
                issues.append(_make_issue("LARGE_REFUND", "Large refund relative to fare", "high", "refund_amount", refund))
        except Exception:
            issues.append(_make_issue("INVALID_REFUND_TYPE", "Refund amount must be numeric", "high", "refund_amount", refund))

    # Aggregate checks
    try:
        net = float(fare or 0) + float(tax or 0) + float(commission or 0) - float(refund or 0)
        if net < 0:
            issues.append(_make_issue("NEGATIVE_NET", "Net amount for transaction is negative", "high", None, net))
    except Exception:
        # ignore net check if types are invalid (already captured above)
        pass

    # Score severity
    severity_weights = {"low": 1, "medium": 2, "high": 3}
    risk_score = sum(severity_weights.get(i.get("severity", "medium"), 2) for i in issues)

    # Provide a compact summary issue if there are many flags
    if risk_score >= 6:
        issues.insert(0, _make_issue("MULTI_ISSUE", f"Multiple issues detected (risk_score={risk_score})", "high", None, None))

    # Attach computed risk score so callers can surface it easily
    for i in issues:
        i.setdefault("meta", {})["risk_score"] = risk_score

    return issues
