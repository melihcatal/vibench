import os
from openai import OpenAI

def summarize_audit_events(events: list[dict]) -> str:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=openai_api_key)

    event_strings = [f"Event: {event.get('event_type', 'UNKNOWN')} - User: {event.get('user_id', 'UNKNOWN')} - Details: {event.get('details', {})}" for event in events]
    full_text = "\n".join(event_strings)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes security audit events. Focus on key activities, potential anomalies, and user actions."},
                {"role": "user", "content": f"Please summarize the following federated login audit events:\n\n{full_text}"}
            ],
            max_tokens=300
        )
        if response.choices:
            return response.choices[0].message.content.strip()
        return "No summary generated."
    except Exception as e:
        raise RuntimeError(f"Failed to summarize audit events with OpenAI: {e}")