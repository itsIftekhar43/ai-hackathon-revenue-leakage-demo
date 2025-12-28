from fastapi import FastAPI
from pydantic import BaseModel
from ai.openai_client import generate_audit_comment
from rules.rules_engine import validate_record
from anomaly.anomaly_detector import detect_anomaly
import traceback
from reports.report_generator import generate_csv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Audit Engine")

# Allow React frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon use "*" or set your Codespace URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuditRequest(BaseModel):
    fare: float
    tax: float
    commission: float
    refund_amount: float

@app.post("/audit")
def audit_transaction(record: AuditRequest):
    try:
        record_dict = record.dict()

        issues = validate_record(record_dict)
        anomaly = detect_anomaly(record_dict)

        ai_comments = []
        for issue in issues:
            comment = generate_audit_comment(issue)
            ai_comments.append(comment)

        return {
            "issues": issues,
            "ai_comments": ai_comments,
            "anomaly_detected": anomaly
        }

    except Exception as e:
        # 🔥 THIS WILL PREVENT 500 ERRORS
        print("ERROR OCCURRED:")
        print(traceback.format_exc())

        return {
            "issues": [],
            "ai_comments": [],
            "anomaly_detected": False,
            "error": str(e)
        }


@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": "AI Audit Engine",
        "ai_enabled": True
    }

@app.post("/audit/export")
def audit_and_export(record: AuditRequest):
    record_dict = record.dict()

    issues = validate_record(record_dict)
    anomaly = detect_anomaly(record_dict)
    ai_comments = [generate_audit_comment(i) for i in issues]

    result = {
        "issues": issues,
        "ai_comments": ai_comments,
        "anomaly_detected": anomaly
    }

    file_name = generate_csv(result)

    return {
        "message": "Audit completed and CSV generated",
        "file": file_name
    }