from __future__ import annotations

from collections import Counter
from typing import Iterable

from openai import OpenAI

from identity_models import AuditRecord

OPENAI_MODEL = "gpt-4o-mini"


def summarize_audit_events(events: Iterable[AuditRecord]) -> str:
    client = OpenAI()
    counts = Counter(event.event_type for event in events)
    prompt = "Summarize these federated-login audit counts: " + ", ".join(
        f"{k}={v}" for k, v in sorted(counts.items())
    )
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content or ""
