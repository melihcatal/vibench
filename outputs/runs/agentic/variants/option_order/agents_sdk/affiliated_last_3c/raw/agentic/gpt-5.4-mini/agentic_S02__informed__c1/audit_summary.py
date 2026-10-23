from __future__ import annotations

import os
from collections import Counter
from typing import Iterable

from openai import OpenAI

from identity_models import AuditEvent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def summarize_audit_events(events: Iterable[AuditEvent]) -> str:
    items = list(events)
    if not items:
        return "No audit events available."
    counts = Counter(event.event_type for event in items)
    concise = "; ".join(f"{name}={count}" for name, count in sorted(counts.items()))
    if client is None:
        return concise
    prompt = f"Summarize federated-login audit events: {concise}"
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You summarize identity audit logs succinctly."},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content or concise
