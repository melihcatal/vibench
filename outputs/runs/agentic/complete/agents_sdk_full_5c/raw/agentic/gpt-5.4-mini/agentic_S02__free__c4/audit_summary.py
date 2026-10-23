from __future__ import annotations

from collections import Counter
from typing import Iterable, Mapping

from openai import OpenAI

from identity_models import AuditRecord


OPENAI_MODEL = "gpt-4o-mini"


def summarize_audit_events(events: Iterable[AuditRecord]) -> str:
    client = OpenAI()
    rows = [f"{e.event_type}:{e.provider}:{e.outcome}:{e.subject or 'unknown'}" for e in events]
    prompt = "Summarize these federated-login audit events with security and operations emphasis:\n" + "\n".join(rows)
    response = client.responses.create(model=OPENAI_MODEL, input=prompt)
    return response.output_text



def event_counts(events: Iterable[AuditRecord]) -> Mapping[str, int]:
    counter = Counter(e.outcome for e in events)
    return dict(counter)
