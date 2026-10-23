from __future__ import annotations

from typing import List

from openai import OpenAI

from observability_models import (
    IncidentSummary,
    NormalizedLogEntry,
    serialize_log_entries,
)


def incident_summary(
    entries: List[NormalizedLogEntry], model: str = "gpt-4.1-mini"
) -> IncidentSummary:
    client = OpenAI(api_key=__import__("os").environ["OPENAI_API_KEY"])
    payload = serialize_log_entries(entries)
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize the incident logs. Return JSON with keys summary, affected_services, top_errors.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": payload}],
            },
        ],
    )
    text = response.output_text
    data = __import__("json").loads(text)
    return IncidentSummary(
        summary=data.get("summary", ""),
        affected_services=list(data.get("affected_services", [])),
        top_errors=list(data.get("top_errors", [])),
    )
