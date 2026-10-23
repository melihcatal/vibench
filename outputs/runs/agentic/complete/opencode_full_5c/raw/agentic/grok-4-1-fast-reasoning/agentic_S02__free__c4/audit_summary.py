import openai
import os
from typing import List
from identity_models import AuditEvent


def summarize_federated_login_audit_events(events: List[AuditEvent]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    events_text = "\n".join(
        f"Event: {e.event_type}, User: {e.user_id or 'unknown'}, Success: {e.success}, IP: {e.ip_address or 'unknown'}"
        for e in events
    )
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize the federated login audit events concisely, noting patterns, failures, and suspicious activity.",
            },
            {"role": "user", "content": f"Events:\n{events_text}"},
        ],
    )
    return completion.choices[0].message.content
