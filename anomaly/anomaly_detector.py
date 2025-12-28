def detect_anomaly(record):
    refund = record.get("refund_amount", 0)
    fare = record.get("fare", 0)

    if fare > 0 and refund > fare * 0.8:
        return True

    return False
