from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from observability_models import NormalizedLogRecord


OPENAI_MODEL = os.getenv("OPENAI_INCIDENT_MODEL", "gpt-4o-mini")


def incident_summary(logs: Iterable[NormalizedLogRecord]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    records: List[NormalizedLogRecord] = list(logs)
    prompt_lines = [
        f"[{record.timestamp}] service={record.service} severity={record.severity} correlation_id={record.correlation_id} message={record.message}"
        for record in records
    ]
    completion = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "Summarize operational error logs for an incident review. Include likely impact, repeated failure patterns, and next investigation steps."},
            {"role": "user", "content": "\n".join(prompt_lines) or "No logs provided."},
        ],
    )
    return completion.output_text
