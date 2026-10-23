from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from identity_models import AuditEvent, summarize_audit_events


OPENAI_MODEL = "gpt-4o-mini"


def summarize_federated_login_audit(events: List[AuditEvent]) -> dict:
    summary = summarize_audit_events(events, provider="auth0")
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    event_lines = [
        f"{event.occurred_at} | {event.event_type} | {event.status} | {event.actor_subject or '-'}"
        for event in events
    ]
    prompt = "\n".join(event_lines) if event_lines else "No events"
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize federated login audit activity and highlight unusual authentication patterns.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "totals": {
            "total_events": summary.total_events,
            "by_type": summary.by_type,
            "by_status": summary.by_status,
        },
        "narrative": response.output_text,
    }
