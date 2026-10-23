import os
import google.generativeai as genai
from typing import List
from identity_client import GOOGLE_API_KEY
from identity_models import LoginAuditEvent

def summarize_audit_events(events: List[LoginAuditEvent]) -> str:
    """
    Summarizes a list of federated-login audit events using Google Gemini API.
    """
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    if not events:
        return "No audit events to summarize."

    event_strings = []
    for event in events:
        event_strings.append(
            f"User {event.user_id} had event '{event.event_type}' at {event.timestamp.isoformat()}. "
            f"Details: {event.details}"
        )
    
    prompt = (
        "Summarize the following federated login audit events, highlighting any unusual patterns "
        "or potential security concerns:

" + "\n".join(event_strings)
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing events with Gemini API: {e}"

if __name__ == "__main__":
    from datetime import datetime, timedelta
    
    # Example usage with dummy events
    sample_events = [
        LoginAuditEvent(
            user_id="user-123", 
            event_type="LOGIN_SUCCESS", 
            timestamp=datetime.utcnow() - timedelta(minutes=10),
            ip_address="192.168.1.1",
            details={"provider": "Auth0", "method": "passwordless"}
        ),
        LoginAuditEvent(
            user_id="user-123", 
            event_type="LOGIN_FAILURE", 
            timestamp=datetime.utcnow() - timedelta(minutes=5),
            ip_address="203.0.113.45",
            details={"provider": "Auth0", "reason": "invalid_credentials"}
        ),
        LoginAuditEvent(
            user_id="user-456", 
            event_type="LOGIN_SUCCESS", 
            timestamp=datetime.utcnow() - timedelta(minutes=2),
            ip_address="192.168.1.1",
            details={"provider": "Auth0", "method": "google"}
        ),
        LoginAuditEvent(
            user_id="user-123", 
            event_type="PROFILE_UPDATE", 
            timestamp=datetime.utcnow() - timedelta(minutes=1),
            ip_address="192.168.1.1",
            details={"field": "email", "old_value": "old@example.com", "new_value": "new@example.com"}
        ),
    ]

    summary = summarize_audit_events(sample_events)
    print("Audit Summary:")
    print(summary)

    no_events_summary = summarize_audit_events([])
    print("\nNo Events Summary:")
    print(no_events_summary)
