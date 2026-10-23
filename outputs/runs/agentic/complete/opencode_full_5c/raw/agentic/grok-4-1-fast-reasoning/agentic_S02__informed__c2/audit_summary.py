from openai import OpenAI
import os
from identity_models import AuditEvent

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_audit_events(events: list[AuditEvent]) -> str:
    events_str = "\n".join(
        [
            f"{e.timestamp}: {e.event_type} (user: {e.user_id}, IP: {e.ip_address}, success: {e.success})"
            for e in events
        ]
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize federated login audit events concisely, highlighting patterns, anomalies, and key statistics.",
            },
            {"role": "user", "content": f"Summarize:\n{events_str}"},
        ],
    )
    return response.choices[0].message.content
