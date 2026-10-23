import os
from openai import OpenAI
from identity_models import AuditEvent
from typing import List


def summarize_audit_events(events: List[AuditEvent]) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt_content = "Summarize the following user login audit events in a brief, human-readable paragraph:\n\n"
    for event in events:
        prompt_content += f"- User {event.user_id} performed '{event.event_name}' at {event.timestamp}. Details: {event.details}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful security analyst assistant.",
                },
                {"role": "user", "content": prompt_content},
            ],
            temperature=0.5,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    sample_events = [
        AuditEvent(
            event_name="login_success",
            user_id="user123",
            timestamp="2024-01-01T12:00:00Z",
            details={"ip": "192.168.1.1"},
        ),
        AuditEvent(
            event_name="login_failure",
            user_id="user123",
            timestamp="2024-01-01T12:01:00Z",
            details={"reason": "wrong_password", "ip": "192.168.1.1"},
        ),
        AuditEvent(
            event_name="profile_update",
            user_id="user456",
            timestamp="2024-01-01T13:00:00Z",
            details={"field": "nickname"},
        ),
    ]
    summary = summarize_audit_events(sample_events)
    print("--- Audit Summary ---")
    print(summary)
