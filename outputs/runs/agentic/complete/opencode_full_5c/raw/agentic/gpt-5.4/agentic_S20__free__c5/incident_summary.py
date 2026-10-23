from __future__ import annotations

import os

from openai import OpenAI

from observability_models import LogQueryResponse


def incident_summary(logs: LogQueryResponse) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    lines = [
        f"{record.timestamp} | {record.status} | {record.message}"
        for record in logs.records
    ]
    prompt = "\n".join(lines) or "No error logs found."
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize error log findings for an incident review in concise operational language.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text
