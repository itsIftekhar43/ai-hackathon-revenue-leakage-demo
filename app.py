from fastapi import FastAPI
from pydantic import BaseModel
from ai.openai_client import generate_audit_comment
from rules.rules_engine import validate_record
from anomaly.anomaly_detector import detect_anomaly

app = FastAPI(title="AI Audit Engine")

class AuditRequest(BaseModel):
    fare: float
    tax: float
    commission: float
    refund_amount: float

@app.post("/audit")
def audit_transaction(record: AuditRequest):
    record_dict = record.dict()

    issues = validate_record(record_dict)
    anomaly = detect_anomaly(record_dict)

    ai_comments = [generate_audit_comment(issue) for issue in issues]

    return {
        "issues": issues,
        "ai_comments": ai_comments,
        "anomaly_detected": anomaly
    }
