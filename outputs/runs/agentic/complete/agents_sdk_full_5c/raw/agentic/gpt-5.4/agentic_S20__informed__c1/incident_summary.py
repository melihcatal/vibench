from __future__ import annotations

import os
from typing import Iterable, Mapping, Any

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_INCIDENT_SUMMARY_MODEL", "gpt-4o-mini")


def incident_summary(records: Iterable[Mapping[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    lines = []
    for record in records:
        lines.append(
            f"[{record.get('timestamp', '')}] severity={record.get('severity', '')} service={record.get('service', '')} message={record.get('message', '')} correlation_id={record.get('correlation_id', '')}"
        )
    prompt = "Summarize these error logs for an incident review, including likely impact, recurring symptoms, and immediate follow-up actions.\n\n" + "\n".join(lines)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    return response.output_text
