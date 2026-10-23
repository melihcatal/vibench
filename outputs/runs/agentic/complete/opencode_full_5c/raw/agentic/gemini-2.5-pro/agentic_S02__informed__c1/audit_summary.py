import os
import google.generativeai as genai
from typing import List
from identity_models import AuditRecord


def summarize_audit_events_with_gemini(audit_records: List[AuditRecord]) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = "Summarize the following federated login audit events, highlighting any suspicious activity:\n\n"
    for record in audit_records:
        prompt += f"- Event: {record.event_type} for User: {record.user_id} at {record.timestamp} with details: {record.details}\n"

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    from datetime import datetime

    sample_records = [
        AuditRecord(
            event_id="evt_1",
            user_id="user_A",
            event_type="login_success",
            timestamp=datetime.now().isoformat(),
            details={"ip": "203.0.113.1"},
        ),
        AuditRecord(
            event_id="evt_2",
            user_id="user_B",
            event_type="login_failed",
            timestamp=datetime.now().isoformat(),
            details={"ip": "198.51.100.2", "reason": "bad_password"},
        ),
        AuditRecord(
            event_id="evt_3",
            user_id="user_A",
            event_type="logout",
            timestamp=datetime.now().isoformat(),
            details={"ip": "203.0.113.1"},
        ),
    ]

    try:
        summary = summarize_audit_events_with_gemini(sample_records)
        print("--- Audit Summary ---")
        print(summary)
    except (ValueError, Exception) as e:
        print(f"Error: {e}")
