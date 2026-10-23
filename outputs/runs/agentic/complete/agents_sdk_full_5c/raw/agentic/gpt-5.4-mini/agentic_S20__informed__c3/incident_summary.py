from __future__ import annotations

import os

from openai import OpenAI

from observability_models import IncidentSummary

OPENAI_MODEL = "gpt-4o-mini"


def summarize_incident(error_log_findings: str) -> IncidentSummary:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=f"Summarize these error-log findings for incident review:\n{error_log_findings}",
    )
    text = response.output_text
    return IncidentSummary(summary=text, key_findings=[line for line in error_log_findings.splitlines() if line.strip()], raw_response=response)
