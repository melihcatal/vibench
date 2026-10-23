import os
import google.generativeai as genai
from identity_models import AuditRecord

# Configure Google Gemini API
# Ensure GOOGLE_API_KEY is set in your environment variables
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def summarize_audit_events(audit_records: list[AuditRecord]) -> str:
    """
    Summarizes a list of federated login audit events using the Gemini API.
    """
    if not audit_records:
        return "No audit records to summarize."

    # Prepare the prompt for the LLM
    event_descriptions = []
    for record in audit_records:
        event_descriptions.append(
            f"Event ID: {record.event_id}, "
            f"Timestamp: {record.timestamp}, "
            f"User: {record.user_id}, "
            f"Type: {record.event_type}, "
            f"Status: {record.status}, "
            f"Details: {record.details}"
        )

    prompt = (
        "Summarize the following federated login audit events. "
        "Highlight any unusual activities, common patterns, or failures:\n\n"
        + "\n".join(event_descriptions)
        + "\n\nSummary:"
    )

    try:
        model = genai.GenerativeModel('gemini-pro') # Using a concrete model identifier
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing audit events with Gemini API: {e}"

if __name__ == "__main__":
    # Example Usage:
    example_records = [
        AuditRecord(
            event_id="1", timestamp="2023-10-27T10:00:00Z", user_id="user123",
            event_type="LOGIN_ATTEMPT", ip_address="192.168.1.1", user_agent="Chrome",
            status="SUCCESS", details={"idp": "Auth0"}
        ),
        AuditRecord(
            event_id="2", timestamp="2023-10-27T10:01:00Z", user_id="user124",
            event_type="LOGIN_ATTEMPT", ip_address="192.168.1.2", user_agent="Firefox",
            status="FAILURE", details={"reason": "Invalid credentials"}
        ),
        AuditRecord(
            event_id="3", timestamp="2023-10-27T10:02:00Z", user_id="user123",
            event_type="LOGIN_ATTEMPT", ip_address="192.168.1.1", user_agent="Chrome",
            status="SUCCESS", details={"idp": "Auth0"}
        ),
    ]
    summary = summarize_audit_events(example_records)
    print(summary)
