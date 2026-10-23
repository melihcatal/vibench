from __future__ import annotations

import os

from openai import OpenAI

from identity_models import AuditRecord, to_dict


def audit_summary(records: list[AuditRecord]) -> dict[str, str | list[dict]]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    events = [to_dict(record) for record in records]
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize federated login audit events with security-relevant highlights.",
            },
            {"role": "user", "content": str(events)},
        ],
    )
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "summary": response.output_text,
        "events": events,
    }
