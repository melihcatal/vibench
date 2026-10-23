from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from identity_models import AuditEvent, summarize_audit_events


OPENAI_AUDIT_MODEL = os.environ.get("OPENAI_AUDIT_MODEL", "gpt-4o-mini")


def summarize_federated_login_audit(events: Iterable[AuditEvent]) -> dict:
    event_list: List[AuditEvent] = list(events)
    aggregate = summarize_audit_events(event_list, provider="OpenAI")
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    lines = [
        f"{event.occurred_at.isoformat()} | {event.event_type} | {event.provider} | {event.user_sub or '-'} | {event.details}"
        for event in event_list
    ]
    prompt = "\n".join(lines) if lines else "No audit events recorded."
    response = client.responses.create(
        model=OPENAI_AUDIT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize federated login audit trails, highlight anomalies, and keep the response concise.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return {
        "provider": "OpenAI",
        "model": OPENAI_AUDIT_MODEL,
        "aggregate": {
            "total_events": aggregate.total_events,
            "by_event_type": aggregate.by_event_type,
            "unique_users": aggregate.unique_users,
            "first_seen": aggregate.first_seen.isoformat() if aggregate.first_seen else None,
            "last_seen": aggregate.last_seen.isoformat() if aggregate.last_seen else None,
        },
        "summary_text": response.output_text,
    }
