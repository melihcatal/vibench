import os
from typing import List
from anthropic import Anthropic
from identity_models import AuditEvent

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def audit_summary(events: List[AuditEvent]) -> str:
    event_str = "\\n".join(
        [
            f"{e.event_type} at {e.timestamp}, user={e.user_id or 'unknown'}, success={e.success}, ip={e.ip_address or 'unknown'}"
            for e in events
        ]
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": f"Summarize these federated login audit events in a concise paragraph:\\n\\n{event_str}",
            }
        ],
    )
    return message.content[0].text
