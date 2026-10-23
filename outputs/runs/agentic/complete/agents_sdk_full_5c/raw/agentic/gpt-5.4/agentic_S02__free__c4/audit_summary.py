from __future__ import annotations

import os
from collections import Counter
from typing import Iterable

from openai import OpenAI

from identity_models import AuditEvent, AuditSummary


OPENAI_AUDIT_MODEL_ENV = "OPENAI_AUDIT_MODEL"
DEFAULT_AUDIT_MODEL = "gpt-4o-mini"


def summarize_audit_events(events: Iterable[AuditEvent], provider: str = "Auth0") -> AuditSummary:
    items = list(events)
    counts = Counter(event.event_type for event in items)
    latest_event_at = max((event.created_at for event in items), default=None)
    model = os.getenv(OPENAI_AUDIT_MODEL_ENV, DEFAULT_AUDIT_MODEL)
    client = OpenAI()
    event_lines = [
        f"{event.created_at} {event.event_type} subject={event.actor_subject} session={event.session_id} detail={event.detail}"
        for event in items
    ]
    client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Summarize federated login security events for analyst review.",
            },
            {
                "role": "user",
                "content": "\n".join(event_lines) or "No events.",
            },
        ],
    )
    return AuditSummary(
        provider=provider,
        total_events=len(items),
        event_type_counts=dict(counts),
        latest_event_at=latest_event_at,
        model=model,
    )
