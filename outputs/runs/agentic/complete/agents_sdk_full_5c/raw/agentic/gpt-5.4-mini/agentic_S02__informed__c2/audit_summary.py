from __future__ import annotations

from collections import Counter
from typing import Iterable, Mapping

import openai

from identity_models import AuditEvent

OPENAI_MODEL = "gpt-4.1-mini"


def summarize_audit_events(events: Iterable[AuditEvent]) -> str:
    client = openai.OpenAI(api_key=None)
    counts = Counter(event.status for event in events)
    prompt = f"Summarize federated-login audit status counts and notable patterns: {dict(counts)}"
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You summarize security audit logs concisely."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
