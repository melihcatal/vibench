import os
import google.generativeai as genai
from identity_models import AuditRecord


def summarize_audit_events(audit_records: list[AuditRecord]) -> str:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("Google API Key must be set as an environment variable (GOOGLE_API_KEY).")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro')

    audit_event_strings = []
    for record in audit_records:
        audit_event_strings.append(
            f"Timestamp: {record.timestamp}, Event Type: {record.event_type}, User ID: {record.user_id}, Details: {record.details}"
        )

    prompt = (
        "Summarize the following federated login audit events. "
        "Identify any anomalies, successful logins, and potential security concerns.\n\n"
        + "\n".join(audit_event_strings)
    )

    response = model.generate_content(prompt)
    return response.text
