from __future__ import annotations

import os
from typing import Any, List

from openai import OpenAI

from observability_models import IncidentSummary

OPENAI_MODEL_ID = os.getenv("OPENAI_MODEL_ID", "gpt-4o-mini")


def summarize_incident(error_records: List[dict[str, Any]]) -> IncidentSummary:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize these error-log findings for incident review:\n" + "\n".join(str(r) for r in error_records[:20])
    response = client.chat.completions.create(
        model=OPENAI_MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
    )
    summary = response.choices[0].message.content or ""
    return IncidentSummary(provider="OpenAI", summary=summary, raw=response)
