from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from observability_models import NormalizedLogRecord


def incident_summary(records: Iterable[NormalizedLogRecord]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    content = "\n".join(
        f"[{record.timestamp}] status={record.status} service={record.service} message={record.message}"
        for record in records
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize error log findings for an incident review in concise operational language.",
            },
            {"role": "user", "content": content},
        ],
    )
    return response.output_text
