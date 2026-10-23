import os
import google.generativeai as genai

from identity_client import get_google_api_key
from identity_models import AuditLogRecord


def summarize_audit_events(audit_records: list[AuditLogRecord]) -> str:
    """Summarizes federated-login audit events using the Google Gemini API."""
    google_api_key = get_google_api_key()
    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro model family

    prompt_text = """
    Review the following federated login audit records and provide a concise summary of the login activity.
    Highlight any unusual patterns or potential security concerns.

    Audit Records:
    """
    for record in audit_records:
        prompt_text += f"- User: {record.user_id}, Event: {record.event_type}, IP: {record.ip_address}, Time: {record.timestamp}, Details: {record.details}\n"

    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"Error summarizing audit events: {e}"
