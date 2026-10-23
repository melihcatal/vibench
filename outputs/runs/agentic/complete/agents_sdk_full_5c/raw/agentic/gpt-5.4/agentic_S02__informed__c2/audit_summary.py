from __future__ import annotations

import json
import os
from typing import Iterable, List

from openai import OpenAI

from identity_models import AuditRecord, AuditSummary, summarize_event_counts, unique_subject_count


OPENAI_MODEL = "gpt-4o-mini"


def summarize_audit_events(records: Iterable[AuditRecord]) -> AuditSummary:
    materialized: List[AuditRecord] = list(records)
    counts = summarize_event_counts(materialized)
    first_seen_at = min((r.occurred_at for r in materialized), default=None)
    last_seen_at = max((r.occurred_at for r in materialized), default=None)

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "provider": "Auth0",
        "task": "Summarize federated login audit events succinctly.",
        "events": [r.__dict__ for r in materialized],
    }
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You summarize identity and login audit trails."},
            {"role": "user", "content": json.dumps(prompt)},
        ],
        temperature=0,
    )
    text = response.choices[0].message.content or ""

    return AuditSummary(
        total_events=len(materialized),
        events_by_type=counts,
        unique_subjects=unique_subject_count(materialized),
        first_seen_at=first_seen_at,
        last_seen_at=last_seen_at,
        provider="auth0",
        model=OPENAI_MODEL,
        raw_summary=text,
    )
