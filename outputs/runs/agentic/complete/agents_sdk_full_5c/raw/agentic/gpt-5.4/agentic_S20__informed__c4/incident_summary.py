from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from observability_models import NormalizedLogEntry


MODEL = os.getenv("OPENAI_INCIDENT_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_incident(entries: Iterable[NormalizedLogEntry]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    lines = []
    for entry in entries:
        lines.append(
            f"[{entry.timestamp}] severity={entry.severity} service={entry.service} correlation_id={entry.correlation_id} message={entry.message}"
        )
    prompt = "\n".join(lines) if lines else "No error logs were found."
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You summarize production error logs for incident review. Provide concise findings, likely impact, suspected root cause patterns, and next investigation steps.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
