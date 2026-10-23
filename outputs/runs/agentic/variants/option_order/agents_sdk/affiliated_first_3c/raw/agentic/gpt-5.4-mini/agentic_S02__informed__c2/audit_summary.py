from __future__ import annotations

import os
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from openai import OpenAI

from identity_models import ProfileClaims

OPENAI_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class AuditSummary:
    summary: str
    counts_by_event: dict[str, int]


def summarize_audit_events(events: Iterable[dict]) -> AuditSummary:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    event_list = list(events)
    counts = Counter(event.get("event_type", "unknown") for event in event_list)
    prompt = f"Summarize these federated-login audit events concisely: {event_list}"
    result = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You summarize security audit events."},
            {"role": "user", "content": prompt},
        ],
    )
    summary = result.choices[0].message.content or ""
    return AuditSummary(summary=summary, counts_by_event=dict(counts))
