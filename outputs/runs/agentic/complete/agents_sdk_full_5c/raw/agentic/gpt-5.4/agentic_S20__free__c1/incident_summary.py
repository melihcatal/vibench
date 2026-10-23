from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from observability_models import LogQueryResponse, logs_to_text


OPENAI_MODEL = os.getenv("OPENAI_INCIDENT_SUMMARY_MODEL", "gpt-4o-mini")


def incident_summary(query_response: LogQueryResponse, incident_title: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    title = incident_title or "Operational incident review"
    transcript = logs_to_text(query_response.records)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "Summarize production error logs for incident review with impact, likely causes, and next actions."},
            {"role": "user", "content": f"Title: {title}\n\nLogs:\n{transcript}"},
        ],
    )
    return response.output_text
