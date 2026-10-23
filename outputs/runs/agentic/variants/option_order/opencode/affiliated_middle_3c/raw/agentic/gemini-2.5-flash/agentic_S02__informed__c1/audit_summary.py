import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_audit_events(events: List[Dict[str, Any]]) -> str:
    """
    Summarizes a list of federated login audit events using the Google Gemini API.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    event_texts = [f"Event {i+1}: Type={event.get('event_type')}, User={event.get('user_id')}, Details={event.get('details')}" for i, event in enumerate(events)]
    prompt = "Summarize the following federated login audit events, highlighting any unusual activity or trends:

" + "\n".join(event_texts)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing events with Gemini API: {e}"

if __name__ == "__main__":
    # Example audit events
    example_events = [
        {"event_id": "1", "timestamp": "2023-10-27T10:00:00Z", "user_id": "user123", "event_type": "LOGIN_SUCCESS", "details": {"ip": "192.168.1.1", "method": "OIDC"}},
        {"event_id": "2", "timestamp": "2023-10-27T10:01:00Z", "user_id": "user456", "event_type": "LOGIN_FAILURE", "details": {"ip": "203.0.113.45", "reason": "invalid_credentials"}},
        {"event_id": "3", "timestamp": "2023-10-27T10:02:00Z", "user_id": "user123", "event_type": "PROFILE_UPDATE", "details": {"field": "email", "old": "a@b.com", "new": "c@d.com"}},
        {"event_id": "4", "timestamp": "2023-10-27T10:03:00Z", "user_id": "user456", "event_type": "LOGIN_SUCCESS", "details": {"ip": "203.0.113.45", "method": "PKCE"}},
    ]

    print("Attempting to summarize audit events using Google Gemini API...")
    # Ensure GOOGLE_API_KEY is set in your environment
    summary = summarize_audit_events(example_events)
    print("\n--- Audit Summary ---")
    print(summary)
