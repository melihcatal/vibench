from __future__ import annotations

from collections import Counter
from typing import Iterable, List, Mapping

from openai import OpenAI

from observability_client import load_client_from_env
from observability_models import QueryRequest


def incident_summary() -> str:
    log_client = load_client_from_env()
    ai_client = OpenAI()
    request = QueryRequest(
        query='severity:error service:checkout-api',
        start_time="2026-01-01T00:00:00Z",
        end_time="2026-01-01T01:00:00Z",
        limit=20,
    )
    findings = log_client.query_logs(request).entries
    sample_text = "\n".join(str(item) for item in findings[:10])
    prompt = f"Summarize the incident from these Datadog logs:\n{sample_text}"
    completion = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""
