from __future__ import annotations

from typing import Dict, Iterable, List

from openai import OpenAI

from observability_models import IncidentSummary

# OpenAI / Azure OpenAI chat completions integration

MODEL_ID = "gpt-4o-mini"


def summarize_incident(error_logs: Iterable[Dict[str, object]], title: str = "Incident review") -> IncidentSummary:
    client = OpenAI()
    logs = list(error_logs)
    prompt = f"Summarize these error logs for incident review:\n{logs}"
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize operational incidents concisely."},
            {"role": "user", "content": prompt},
        ],
    )
    summary = completion.choices[0].message.content or ""
    severity = "high" if any(str(item.get("severity", "")).upper() == "ERROR" for item in logs if isinstance(item, dict)) else "medium"
    return IncidentSummary(title=title, severity=severity, summary=summary, evidence=logs)
