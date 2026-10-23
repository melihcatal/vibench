from __future__ import annotations

from typing import Iterable, List

from observability_client import openai_post
from observability_models import RetrievedLog


def incident_summary(logs: Iterable[RetrievedLog]) -> str:
    rendered_logs: List[str] = []
    for log in logs:
        rendered_logs.append(
            f"[{log.timestamp}] {log.status or 'unknown'} {log.service or 'unknown'} {log.message}"
        )
    prompt = (
        "Summarize these production error logs for incident review with impact, likely scope, and immediate follow-up actions.\n\n"
        + "\n".join(rendered_logs)
    )
    response = openai_post(
        "responses",
        {
            "model": "gpt-5.4",
            "input": prompt,
        },
    )
    return response["output"][0]["content"][0]["text"]
