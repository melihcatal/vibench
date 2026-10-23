import os
import google.generativeai as genai
from typing import List
from identity_models import AuditEvent

def summarize_audit_events(audit_events: List[AuditEvent]) -> str:
    """
    Summarizes a list of federated login audit events using Google Gemini API.

    Args:
        audit_events: A list of AuditEvent objects.

    Returns:
        A string summary of the audit events.
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("Missing GOOGLE_API_KEY environment variable.")

    genai.configure(api_key=GOOGLE_API_KEY)

    # Use the generative model for text summarization
    model = genai.GenerativeModel('gemini-pro') # Concrete model identifier

    event_strings = []
    for event in audit_events:
        event_strings.append(f"Event ID: {event.event_id}, User ID: {event.user_id}, Type: {event.event_type}, Timestamp: {event.timestamp}")
        if event.metadata:
            event_strings.append(f"  Metadata: {event.metadata}")

    prompt = """
    Summarize the following federated login audit events. 
    Highlight any unusual activity or trends. If there are no events, state that.

    Audit Events:
    """
    prompt += "\n".join(event_strings) if event_strings else "No audit events provided."

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage
    os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"

    dummy_events = [
        AuditEvent(
            event_id="evt_001",
            user_id="user_abc",
            timestamp="2023-10-27T10:00:00Z",
            event_type="login_success",
            ip_address="192.168.1.1",
            metadata={'auth_provider': 'Auth0'}
        ),
        AuditEvent(
            event_id="evt_002",
            user_id="user_xyz",
            timestamp="2023-10-27T10:05:00Z",
            event_type="login_failure",
            ip_address="192.168.1.2",
            metadata={'auth_provider': 'Auth0', 'reason': 'invalid_credentials'}
        ),
        AuditEvent(
            event_id="evt_003",
            user_id="user_abc",
            timestamp="2023-10-27T10:15:00Z",
            event_type="token_refresh",
            ip_address="192.168.1.1",
            metadata={'auth_provider': 'Auth0'}
        ),
    ]

    try:
        summary = summarize_audit_events(dummy_events)
        print("\n--- Audit Summary ---")
        print(summary)
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Error summarizing events: {e}")
