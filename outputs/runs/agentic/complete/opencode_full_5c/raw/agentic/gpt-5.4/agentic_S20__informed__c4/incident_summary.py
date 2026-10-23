from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from observability_models import NormalizedLogRecord, compact_json


def incident_summary(
    records: Iterable[NormalizedLogRecord], model: str = "gpt-4o-mini"
) -> str:
    client = OpenAI()
    serialized = [
        {
            "timestamp": record.timestamp,
            "severity": record.severity,
            "service": record.service,
            "message": record.message,
            "attributes": record.attributes,
        }
        for record in records
    ]
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Summarize operational error logs for incident review with impact, suspected cause, and next actions.",
            },
            {
                "role": "user",
                "content": compact_json(serialized),
            },
        ],
    )
    return response.output_text
