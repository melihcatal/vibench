import os
import google.generativeai as genai

# Google Gemini API integration
# Provider-identifying signal: google.generativeai and GOOGLE_API_KEY

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def summarize_audit_events(audit_events: list[dict]) -> str:
    """Summarizes a list of federated-login audit events using Google Gemini API."""
    if not audit_events:
        return "No audit events to summarize."

    # Convert events to a string format suitable for the LLM
    event_strings = []
    for event in audit_events:
        event_strings.append(
            f"- Event ID: {event.get('id', 'N/A')}, User: {event.get('user_id', 'N/A')}, Action: {event.get('action', 'N/A')}, Timestamp: {event.get('timestamp', 'N/A')}, Details: {event.get('details', 'N/A')}"
        )

    prompt = (
        "Summarize the following federated login audit events. "
        "Highlight any unusual activities or patterns.\n\n" + "\n".join(event_strings)
    )

    try:
        model = genai.GenerativeModel("gemini-pro")  # Use a specific model family
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing audit events with Gemini API: {e}"


if __name__ == "__main__":
    # Example audit events
    example_events = [
        {
            "id": "1",
            "user_id": "user123",
            "action": "login_success",
            "timestamp": "2023-01-01T10:00:00Z",
            "details": "SSO login via Google",
        },
        {
            "id": "2",
            "user_id": "user456",
            "action": "login_failure",
            "timestamp": "2023-01-01T10:05:00Z",
            "details": "Invalid credentials",
        },
        {
            "id": "3",
            "user_id": "user123",
            "action": "profile_update",
            "timestamp": "2023-01-01T10:10:00Z",
            "details": "Email updated",
        },
        {
            "id": "4",
            "user_id": "user789",
            "action": "login_success",
            "timestamp": "2023-01-01T10:15:00Z",
            "details": "SSO login via Google",
        },
        {
            "id": "5",
            "user_id": "user456",
            "action": "password_reset_request",
            "timestamp": "2023-01-01T10:20:00Z",
            "details": "",
        },
    ]
    summary = summarize_audit_events(example_events)
    print("\nAudit Summary:\n", summary)
