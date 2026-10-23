from __future__ import annotations

import os
from collections import Counter
from typing import Any

from openai import OpenAI

from identity_models import AuditRecord, audit_record_to_document


def summarize_audit_events(records: list[AuditRecord]) -> dict[str, Any]:
    documents = [audit_record_to_document(record) for record in records]
    outcome_counts = Counter(record.outcome or "unknown" for record in records)
    provider_counts = Counter(record.provider for record in records)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "events": documents,
        "outcome_counts": dict(outcome_counts),
        "provider_counts": dict(provider_counts),
        "task": "Summarize federated login audit events and highlight anomalies.",
    }
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "user", "content": [{"type": "input_text", "text": str(prompt)}]}
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
        "outcome_counts": dict(outcome_counts),
        "provider_counts": dict(provider_counts),
    }
