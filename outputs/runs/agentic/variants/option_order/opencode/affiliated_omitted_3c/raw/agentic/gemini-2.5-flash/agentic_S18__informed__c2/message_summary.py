import os
from openai import OpenAI
from messaging_models import EventMessage


def summarize_message(event: EventMessage) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"Summarize the following event message in one concise sentence:\n\n{event.to_json_string()}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a concrete model identifier
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes event messages.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    # Example usage
    event = EventMessage(
        message_id="summary-test-1",
        payload={
            "user": {"id": "user123", "name": "John Doe"},
            "action": "login",
            "ip_address": "192.168.1.1",
            "timestamp": "2026-04-20T11:00:00Z",
        },
        attributes={"source_service": "auth_service"},
    )
    print(f"Summarizing event with ID: {event.message_id}...")
    summary = summarize_message(event)
    print(f"Summary: {summary}")
