import os
import google.generativeai as genai
from typing import List
from identity_models import AuditRecord


def summarize_audit_events(audit_records: List[AuditRecord]) -> str:
    """Summarizes federated-login audit events using the Google Gemini API."""
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel("gemini-pro")

    audit_event_strings = []
    for record in audit_records:
        audit_event_strings.append(
            f"Timestamp: {record.timestamp}, Event: {record.event_type}, User ID: {record.user_id}, "
            f"IP: {record.ip_address}, User Agent: {record.user_agent}, Details: {record.details}"
        )

    prompt = "Summarize the following federated login audit events, highlighting any unusual patterns or errors:\n\n"
    prompt += "\n".join(audit_event_strings)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing audit events with Gemini API: {e}")
        return "Failed to generate summary."


if __name__ == "__main__":
    # Example usage
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
    #
    # from datetime import datetime
    # mock_audit_records = [
    #     AuditRecord(
    #         timestamp=datetime.now().isoformat(),
    #         event_type="LOGIN_SUCCESS",
    #         user_id="user123",
    #         ip_address="192.168.1.1",
    #         user_agent="Mozilla/5.0",
    #         details={'provider': 'Auth0', 'method': 'OIDC'}
    #     ),
    #     AuditRecord(
    #         timestamp=datetime.now().isoformat(),
    #         event_type="LOGIN_FAILURE",
    #         user_id="user456",
    #         ip_address="192.168.1.2",
    #         user_agent="Chrome",
    #         details={'provider': 'Auth0', 'error': 'invalid_credentials'}
    #     )
    # ]
    #
    # try:
    #     summary = summarize_audit_events(mock_audit_records)
    #     print("\nAudit Summary:")
    #     print(summary)
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass  # placeholder to avoid runtime error if __name__ is run without actual env vars
