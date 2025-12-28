def validate_record(record):
    issues = []

    if record.get("fare", 0) <= 0:
        issues.append("Invalid fare amount")

    if record.get("tax", 0) < 0:
        issues.append("Negative tax detected")

    if record.get("commission", 0) > record.get("fare", 0):
        issues.append("Commission exceeds fare")

    return issues
