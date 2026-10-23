from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from observability_models import NormalizedLogEntry


OPENAI_MODEL = os.getenv("OPENAI_INCIDENT_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_incident(logs: Iterable[NormalizedLogEntry]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    lines = [f"{entry.timestamp} | {entry.message}" for entry in logs]
    prompt = "\n".join(lines) or "No error logs found."
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You summarize operational incidents from application error logs for incident review.",
            },
            {
                "role": "user",
                "content": f"Summarize the likely incident, scope, user impact, and next steps based on these logs:\n{prompt}",
            },
        ],
    )
    return response.choices[0].message.content or ""
