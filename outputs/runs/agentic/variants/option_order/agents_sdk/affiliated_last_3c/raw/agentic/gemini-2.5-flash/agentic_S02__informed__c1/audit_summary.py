import os
import google.generativeai as genai
import json
from identity_client import get_gemini_config
from identity_models import LoginAuditEvent

def summarize_audit_events(audit_events: list[LoginAuditEvent]):
    config = get_gemini_config()
    api_key = config["GOOGLE_API_KEY"]
    model_id = config["GEMINI_MODEL_ID"]

    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        print("Error: GOOGLE_API_KEY is not set or is default. Please configure your API key.")
        return "Gemini API key not configured."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_id)

    event_strings = [json.dumps(event.to_dict()) for event in audit_events]
    prompt = f"""
    Summarize the following federated login audit events, highlighting any anomalies or key trends.
    Provide a concise summary in a few paragraphs.

    Audit Events:
    {json.dumps(event_strings, indent=2)}
    """

    try:
        response = model.generate_content(prompt)
        summary = response.text
        print("Successfully summarized audit events using Google Gemini API.")
        return summary
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error summarizing audit events: {e}"

if __name__ == "__main__":
    # Example usage
    sample_events = [
        LoginAuditEvent(
            event_id="evt_1",
            timestamp="2023-10-27T10:00:00Z",
            user_id="user_abc",
            event_type="login_success",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/118.0.0.0",
            status="success",
            details={"provider": "Auth0", "method": "passwordless"}
        ),
        LoginAuditEvent(
            event_id="evt_2",
            timestamp="2023-10-27T10:01:00Z",
            user_id="user_xyz",
            event_type="login_failure",
            ip_address="203.0.113.45",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
            status="failure",
            details={"provider": "Google", "error": "invalid_grant"}
        ),
        LoginAuditEvent(
            event_id="evt_3",
            timestamp="2023-10-27T10:05:00Z",
            user_id="user_abc",
            event_type="profile_update",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/118.0.0.0",
            status="success",
            details={"field": "email", "old_value": "old@example.com", "new_value": "new@example.com"}
        )
    ]
    summary = summarize_audit_events(sample_events)
    print("\n--- Summary ---")
    print(summary)
