from __future__ import annotations

from collections import Counter
from typing import Iterable, Mapping

from openai import OpenAI

from identity_models import AuditEvent

OPENAI_MODEL = "gpt-4o-mini"


def summarize_audit_events(events: Iterable[AuditEvent]) -> str:
    client = OpenAI()
    event_list = list(events)
    counts = Counter(event.event_type for event in event_list)
    prompt = {
        "model": OPENAI_MODEL,
        "counts": dict(counts),
        "events": [event.__dict__ for event in event_list],
    }
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Summarize federated-login audit events succinctly."},
            {"role": "user", "content": str(prompt)},
        ],
    )
    return response.choices[0].message.content or ""
