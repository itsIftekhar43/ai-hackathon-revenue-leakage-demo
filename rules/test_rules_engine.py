from rules.rules_engine import validate_record


def test_validate_simple_failure():
    rec = {"fare": 100, "tax": -10, "commission": 60, "refund_amount": 85}
    issues = validate_record(rec)

    codes = [i["code"] for i in issues]
    assert "NEG_TAX" in codes
    assert "COMMISSION_EXCEEDS_FARE" in codes or "HIGH_COMMISSION_RATIO" in codes
    assert any(i["code"] == "LARGE_REFUND" for i in issues)


if __name__ == "__main__":
    test_validate_simple_failure()
    print("rules_engine tests passed")
