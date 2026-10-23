from __future__ import annotations

import os

from anthropic import Anthropic

from identity_models import AuditRecord


def audit_summary(records: list[AuditRecord | dict]) -> str:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    normalized = [
        record.to_dict() if isinstance(record, AuditRecord) else record
        for record in records
    ]
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"Summarize these federated login audit events with focus on failures, anomalies, and volume trends: {normalized}",
            }
        ],
    )
    return "".join(
        block.text for block in response.content if getattr(block, "type", "") == "text"
    )
