import os
import google.generativeai as genai
from identity_client import get_google_gemini_api_key
from typing import List, Dict, Any


def summarize_audit_events(audit_events: List[Dict[str, Any]]) -> str:
    api_key = get_google_gemini_api_key()
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")  # Provider-specific model ID

    event_strings = [
        f"Event Type: {event.get('event_type')}, User ID: {event.get('user_id')}, Details: {event.get('details')}"
        for event in audit_events
    ]
    prompt = (
        "Please summarize the following federated login audit events, highlighting any unusual activity:\n\n"
        + "\n".join(event_strings)
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing audit events with Gemini API: {e}"


if __name__ == "__main__":
    # Example usage: simulate a list of audit events
    os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_GEMINI_API_KEY"

    sample_audit_events = [
        {
            "event_type": "login_success",
            "user_id": "user123",
            "details": {"ip": "192.168.1.1", "provider": "Auth0"},
        },
        {
            "event_type": "login_failure",
            "user_id": "user456",
            "details": {"ip": "10.0.0.5", "reason": "invalid_credentials"},
        },
        {
            "event_type": "profile_update",
            "user_id": "user123",
            "details": {
                "field": "email",
                "old": "a@example.com",
                "new": "b@example.com",
            },
        },
        {
            "event_type": "unusual_login_location",
            "user_id": "user789",
            "details": {
                "ip": "203.0.113.45",
                "country": "Nigeria",
                "previous_country": "USA",
            },
        },
    ]

    print("Summarizing audit events...")
    summary = summarize_audit_events(sample_audit_events)
    print("\nAudit Summary:")
    print(summary)
