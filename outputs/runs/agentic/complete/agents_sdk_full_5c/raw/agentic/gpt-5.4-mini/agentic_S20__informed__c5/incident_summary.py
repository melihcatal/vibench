from __future__ import annotations

from openai import OpenAI

from observability_client import build_client_from_env
from observability_models import LogQuery

MODEL_ID = "gpt-4o-mini"


def incident_summary() -> str:
    client = build_client_from_env()
    logs = client.query_logs(LogQuery(severity="error", field_filters={"service": "checkout-api"}, limit=10)).results
    payload = "\n".join(entry.get("message", "") for entry in logs)
    llm = OpenAI()
    response = llm.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize incident log findings for review."},
            {"role": "user", "content": payload or "No errors found."},
        ],
    )
    return response.choices[0].message.content or ""
