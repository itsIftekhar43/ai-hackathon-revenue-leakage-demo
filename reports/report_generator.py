import csv
from datetime import datetime

def generate_csv(audit_result: dict) -> str:
    filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Issue", "AI Comment", "Anomaly Detected"])

        for i, issue in enumerate(audit_result["issues"]):
            writer.writerow([
                issue,
                audit_result["ai_comments"][i],
                audit_result["anomaly_detected"]
            ])

    return filename
