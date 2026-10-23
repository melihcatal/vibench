import os
import openai
from typing import List
from .identity_models import AuditEvent, asdict


def summarize_federated_login_audits(events: List[AuditEvent]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    event_str = "\n".join(
        [
            f"{e.event_type} at {e.timestamp} (success: {e.success}): {e.details}"
            for e in events
        ]
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Provide a concise summary of these federated login audit events, highlighting key patterns, failures, and user activities.",
            },
            {"role": "user", "content": event_str},
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
