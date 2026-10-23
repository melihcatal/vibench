from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_INCIDENT_SUMMARY_MODEL", "gpt-4.1-mini")


def incident_summary(logs: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    lines = []
    for log in logs:
        lines.append(
            f"[{log.get('timestamp')}] service={log.get('service')} severity={log.get('severity')} correlation_id={log.get('correlation_id')} message={log.get('message')}"
        )
    prompt = (
        "Summarize these incident-related logs for an incident review, including impact, likely cause, and next actions:\n"
        + "\n".join(lines)
    )
    response = client.responses.create(model=OPENAI_MODEL, input=prompt)
    return response.output_text
