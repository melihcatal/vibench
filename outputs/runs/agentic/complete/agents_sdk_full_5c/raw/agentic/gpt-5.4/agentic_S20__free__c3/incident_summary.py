from __future__ import annotations

from collections import Counter
from typing import Iterable

from openai import OpenAI

from observability_models import IncidentSummary, NormalizedLogRecord


OPENAI_MODEL = "gpt-4o-mini"


def incident_summary(records: Iterable[NormalizedLogRecord]) -> IncidentSummary:
    items = list(records)
    services = [r.service for r in items if r.service]
    counts = Counter(services)
    prompt = "\n".join(
        f"[{r.timestamp}] service={r.service} level={r.level} correlation_id={r.correlation_id} message={r.message}"
        for r in items[:50]
    )
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize incident-relevant findings from application error logs in 3 concise bullet points.",
            },
            {"role": "user", "content": prompt or "No error logs found."},
        ],
    )
    top_services = [name for name, _ in counts.most_common(5)]
    return IncidentSummary(
        summary=response.output_text,
        total_errors=len(items),
        affected_services=top_services,
    )
