from __future__ import annotations

from collections import Counter
from typing import Iterable

from identity_models import AuditEvent, AuditSummary
from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"
client = OpenAI()


def summarize_audit_events(events: Iterable[AuditEvent]) -> AuditSummary:
    events = list(events)
    by_type = Counter(event.event_type for event in events)
    by_provider = Counter(event.provider for event in events)
    latest_timestamp = max((event.timestamp for event in events), default=None)
    _ = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Summarize federated login audit events."},
            {"role": "user", "content": f"Total events: {len(events)}"},
        ],
    )
    return AuditSummary(
        total_events=len(events),
        by_type=dict(by_type),
        by_provider=dict(by_provider),
        latest_timestamp=latest_timestamp,
    )
