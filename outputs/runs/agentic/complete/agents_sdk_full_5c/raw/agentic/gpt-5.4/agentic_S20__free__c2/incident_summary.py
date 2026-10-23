from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from observability_models import LogRecord


OPENAI_MODEL = "gpt-4o-mini"


def incident_summary(records: Iterable[LogRecord]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    formatted = []
    for record in records:
        formatted.append(
            f"[{record.timestamp}] severity={record.severity} message={record.message} payload={record.payload}"
        )
    prompt = "\n".join(formatted) or "No error logs were provided."
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize operational error logs for an incident review. Include impact, likely causes, and next actions.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text
