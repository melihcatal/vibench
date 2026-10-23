from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from observability_models import IncidentSummaryResult, LogQueryResult

MODEL_NAME = "gpt-4o-mini"



def incident_summary(logs: Iterable[LogQueryResult]) -> IncidentSummaryResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    rendered = []
    for log in logs:
        rendered.append(f"[{log.timestamp}] severity={log.severity} service={log.service} correlation_id={log.correlation_id} message={log.message}")
    prompt = "Summarize the incident-relevant findings from these error logs. Include likely impact, repeated patterns, and next investigation steps.\n\n" + "\n".join(rendered)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You summarize operational incidents for SRE review."},
            {"role": "user", "content": prompt},
        ],
    )
    summary = response.choices[0].message.content or ""
    return IncidentSummaryResult(
        summary=summary,
        contributing_errors=[log.message for log in logs],
        provider_model=MODEL_NAME,
    )
