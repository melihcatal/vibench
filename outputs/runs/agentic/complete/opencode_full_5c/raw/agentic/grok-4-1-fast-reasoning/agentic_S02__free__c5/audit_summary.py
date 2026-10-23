import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_federated_login_audits(audit_events: list[dict]) -> str:
    events_str = "\n".join(
        f"{event.get('timestamp', 'N/A')}: {event.get('event_type', 'N/A')} - {event.get('details', '')}"
        for event in audit_events
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize federated login audit events concisely, highlighting key patterns, successes, failures, and anomalies.",
            },
            {"role": "user", "content": events_str},
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
