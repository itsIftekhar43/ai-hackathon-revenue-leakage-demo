from fastapi import FastAPI
from ai.openai_client import generate_audit_comment
from rules.rules_engine import validate_record
from anomaly.anomaly_detector import detect_anomaly

app = FastAPI(title="AI Audit Engine")

@app.post("/audit")
def audit_transaction(record: dict):
    issues = validate_record(record)
    anomaly = detect_anomaly(record)

    ai_comments = [generate_audit_comment(issue) for issue in issues]

    return {
        "issues": issues,
        "ai_comments": ai_comments,
        "anomaly_detected": anomaly
    }
