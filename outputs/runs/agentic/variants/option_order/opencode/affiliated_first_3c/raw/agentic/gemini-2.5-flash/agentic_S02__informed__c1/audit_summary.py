import os
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")


def summarize_audit_events(audit_events: list[dict]) -> str:
    if not GOOGLE_API_KEY:
        raise ValueError("Missing GOOGLE_API_KEY environment variable.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        "Summarize the following federated login audit events. "
        "Highlight any unusual activities or potential security concerns.\n\n"
        f"Audit Events: {audit_events}"
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing audit events with Gemini API: {e}")
        return "Failed to generate summary."


if __name__ == "__main__":
    example_events = [
        {
            "timestamp": "2023-10-27T10:00:00Z",
            "user": "user1",
            "event": "login_success",
            "ip": "192.168.1.1",
        },
        {
            "timestamp": "2023-10-27T10:05:00Z",
            "user": "user2",
            "event": "login_failure",
            "reason": "invalid_password",
            "ip": "192.168.1.2",
        },
        {
            "timestamp": "2023-10-27T10:10:00Z",
            "user": "user1",
            "event": "profile_update",
            "field": "email",
        },
        {
            "timestamp": "2023-10-27T10:15:00Z",
            "user": "user3",
            "event": "login_success",
            "ip": "203.0.113.45",
            "country": "UNKNOWN",
        },
    ]
    summary = summarize_audit_events(example_events)
    print(summary)
