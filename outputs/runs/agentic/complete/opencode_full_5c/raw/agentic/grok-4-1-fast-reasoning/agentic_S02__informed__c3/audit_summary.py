from typing import List
from openai import OpenAI
import os
from identity_models import AuditEvent


def summarize_audit_events(events: List[AuditEvent]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    events_str = "\\n".join(
        [
            f"{e.timestamp}: {e.event_type} ({'success' if e.success else 'failure'}) for user {e.user_id or 'unknown'}"
            for e in events
        ]
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize federated login audit events concisely, highlighting patterns, anomalies, and key insights.",
            },
            {"role": "user", "content": f"Summarize these events:\\n{events_str}"},
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
