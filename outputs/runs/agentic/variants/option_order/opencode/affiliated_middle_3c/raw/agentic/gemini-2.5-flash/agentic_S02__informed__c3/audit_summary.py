import os
import google.generativeai as genai

from identity_models import AuditRecord

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def summarize_audit_events(audit_records: list[AuditRecord]) -> str:
    """Summarizes a list of federated-login audit events using the Google Gemini API.

    Args:
        audit_records: A list of AuditRecord objects.

    Returns:
        A string summary of the audit events.
    """
    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model identifier

    event_strings = []
    for record in audit_records:
        event_strings.append(
            f"Event ID: {record.event_id}, Timestamp: {record.timestamp}, "
            f"Type: {record.event_type}, User ID: {record.user_id}, "
            f"IP: {record.ip_address}, Details: {record.details}"
        )

    prompt = (
        "Summarize the following federated login audit events, highlighting any unusual activity or potential security concerns:\n\n"
        + "\n".join(event_strings)
    )

    response = model.generate_content(prompt)
    return response.text
