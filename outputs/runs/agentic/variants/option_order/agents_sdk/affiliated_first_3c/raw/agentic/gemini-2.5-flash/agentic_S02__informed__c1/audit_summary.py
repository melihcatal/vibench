import os
import google.generativeai as genai
from typing import List, Dict, Any

# Configure Google Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def summarize_audit_events(audit_events: List[Dict[str, Any]]) -> str:
    """Summarizes a list of federated-login audit events using Google Gemini API."""
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not set for audit summary."

    model = genai.GenerativeModel("gemini-pro") # Using a concrete model identifier

    # Prepare a prompt for the LLM
    event_strings = [str(event) for event in audit_events]
    prompt = f"""Summarize the following federated login audit events, highlighting any anomalies or key trends:

{  '\n'.join(event_strings)}

Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing audit events with Gemini API: {e}"

if __name__ == "__main__":
    # Example usage (dummy events)
    example_events = [
        {
            "event_id": "123",
            "timestamp": "2023-10-27T10:00:00Z",
            "user_id": "user123",
            "event_type": "login_success",
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "details": {"provider": "google"}
        },
        {
            "event_id": "124",
            "timestamp": "2023-10-27T10:01:00Z",
            "user_id": "user123",
            "event_type": "login_failure",
            "ip_address": "1.2.3.4", # Different IP
            "user_agent": "Python/requests",
            "details": {"provider": "google", "reason": "invalid_credentials"}
        },
        {
            "event_id": "125",
            "timestamp": "2023-10-27T10:02:00Z",
            "user_id": "user456",
            "event_type": "login_success",
            "ip_address": "192.168.1.5",
            "user_agent": "Chrome/90",
            "details": {"provider": "auth0"}
        },
    ]

    if GEMINI_API_KEY:
        summary = summarize_audit_events(example_events)
        print("Audit Summary:")
        print(summary)
    else:
        print("Please set the GEMINI_API_KEY environment variable to run this example.")
