import os
import google.generativeai as genai

# Configure Google Gemini API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

def summarize_audit_events(audit_events: list[dict]) -> str:
    """Summarizes a list of federated login audit events using the Google Gemini API."""
    if not audit_events:
        return "No audit events to summarize."

    # Prepare the prompt for the Gemini API
    event_strings = [f"- Event ID: {event.get('event_id')}, Type: {event.get('event_type')}, User: {event.get('user_id')}, Timestamp: {event.get('timestamp')}, Provider: {event.get('provider')}, Details: {event.get('details')}"
                      for event in audit_events]
    
    prompt = """Summarize the following federated login audit events. 
    Highlight any unusual patterns, frequent failures, or successful login trends.

    """ + "\n".join(event_strings) + """

    Summary:"""

    try:
        # Use a generative model (e.g., gemini-pro)
        model = genai.GenerativeModel('gemini-pro') # Provider-specific model ID
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing audit events with Gemini API: {e}")
        return "Failed to summarize audit events."

if __name__ == "__main__":
    example_events = [
        {
            "event_id": "aud-123",
            "user_id": "user-abc",
            "timestamp": "2023-10-27T10:00:00Z",
            "event_type": "LOGIN_SUCCESS",
            "provider": "Auth0",
            "details": {"ip_address": "192.168.1.1", "device": "Chrome on Mac"}
        },
        {
            "event_id": "aud-124",
            "user_id": "user-xyz",
            "timestamp": "2023-10-27T10:05:00Z",
            "event_type": "LOGIN_FAILURE",
            "provider": "Auth0",
            "details": {"ip_address": "10.0.0.5", "reason": "MFA_REQUIRED"}
        },
        {
            "event_id": "aud-125",
            "user_id": "user-abc",
            "timestamp": "2023-10-27T10:10:00Z",
            "event_type": "TOKEN_EXCHANGE",
            "provider": "Auth0",
            "details": {"client_id": "some-client", "scope": "openid profile"}
        },
    ]
    summary = summarize_audit_events(example_events)
    print("\n--- Audit Summary ---")
    print(summary)
