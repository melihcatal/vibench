from __future__ import annotations

from openai import OpenAI

from observability_models import LogQueryResponse


MODEL_ID = "gpt-4o-mini"


def incident_summary(error_facts: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize log incidents for review."},
            {"role": "user", "content": error_facts},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
