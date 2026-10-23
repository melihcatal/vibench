from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from observability_models import NormalizedLogRecord


OPENAI_MODEL = os.getenv("OPENAI_INCIDENT_SUMMARY_MODEL", "gpt-4o-mini")


def incident_summary(logs: Iterable[NormalizedLogRecord]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    lines: List[str] = []
    for log in logs:
        lines.append(f"[{log.timestamp}] {log.service or 'unknown'} {log.status}: {log.message}")
    prompt = "Summarize the following error logs for an incident review, including likely impact, recurring patterns, and immediate follow-up actions.\n\n" + "\n".join(lines)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    return response.output_text
