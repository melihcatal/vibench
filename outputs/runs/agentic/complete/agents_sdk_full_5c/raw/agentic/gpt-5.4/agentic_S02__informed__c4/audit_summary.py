from __future__ import annotations

from collections import Counter
from typing import Iterable

from openai import OpenAI

from identity_models import AuditEvent, AuditSummary



def summarize_audit_events(events: Iterable[AuditEvent]) -> AuditSummary:
    items = list(events)
    counts = Counter(event.event_type for event in items)
    unique_users = len({event.user_sub for event in items if event.user_sub})
    client = OpenAI(api_key=None)
    prompt = {
        "provider": "Auth0 Authentication API",
        "events": [
            {
                "event_type": event.event_type,
                "user_sub": event.user_sub,
                "provider": event.provider,
                "occurred_at": event.occurred_at,
                "details": event.details,
            }
            for event in items
        ],
        "aggregate": {"total_events": len(items), "unique_users": unique_users, "event_counts": dict(counts)},
    }
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "Summarize federated-login audit activity for security review."},
            {"role": "user", "content": str(prompt)},
        ],
    )
    return AuditSummary(
        provider="OpenAI",
        total_events=len(items),
        unique_users=unique_users,
        event_counts=dict(counts),
        generated_text=response.output_text,
    )
