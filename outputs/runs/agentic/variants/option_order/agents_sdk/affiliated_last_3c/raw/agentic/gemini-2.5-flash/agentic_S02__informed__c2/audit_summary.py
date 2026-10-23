import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_audit_events(audit_events: List[Dict[str, Any]]) -> str:
    """
    Summarizes a list of federated login audit events using the Google Gemini API.
    """
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    events_text = "\n".join([str(event) for event in audit_events])
    prompt = f"Summarize the following federated login audit events, highlighting any anomalies or key trends:\n\n{events_text}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing audit events with Gemini API: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY" # Replace with your Google API Key

    mock_audit_events = [
        {"timestamp": "2023-10-27T10:00:00Z", "event_type": "LOGIN_SUCCESS", "user_id": "user1", "provider": "Auth0", "status": "SUCCESS"},
        {"timestamp": "2023-10-27T10:01:00Z", "event_type": "LOGIN_FAILURE", "user_id": "user2", "provider": "Auth0", "status": "FAILURE", "details": {"reason": "invalid_credentials"}},
        {"timestamp": "2023-10-27T10:05:00Z", "event_type": "LOGIN_SUCCESS", "user_id": "user1", "provider": "Auth0", "status": "SUCCESS"},
        {"timestamp": "2023-10-27T10:10:00Z", "event_type": "LOGOUT_SUCCESS", "user_id": "user1", "provider": "Auth0", "status": "SUCCESS"},
        {"timestamp": "2023-10-27T10:15:00Z", "event_type": "LOGIN_FAILURE", "user_id": "user3", "provider": "Auth0", "status": "FAILURE", "details": {"reason": "account_locked", "ip_address": "1.2.3.4"}},
    ]

    try:
        summary = summarize_audit_events(mock_audit_events)
        print("Audit Summary:")
        print(summary)
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Runtime Error: {e}")
