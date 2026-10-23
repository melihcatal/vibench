from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from identity_models import AuditRecord, summarize_audit_records


OPENAI_MODEL = os.getenv("OPENAI_AUDIT_MODEL", "gpt-4o-mini")


def summarize_federated_login_audit(records: Iterable[AuditRecord]) -> dict:
    record_list: List[AuditRecord] = list(records)
    deterministic = summarize_audit_records(record_list, provider="auth0")
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "provider": "auth0",
        "totals": deterministic.total_events,
        "counts": deterministic.event_type_counts,
        "unique_subjects": deterministic.unique_subjects,
        "window_start": deterministic.window_start,
        "window_end": deterministic.window_end,
    }
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "Summarize federated login audit events in concise JSON with keys summary and risk_signals."},
            {"role": "user", "content": str(prompt)},
        ],
    )
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "summary": response.output_text,
        "totals": deterministic.total_events,
        "event_type_counts": deterministic.event_type_counts,
    }
