from __future__ import annotations

import os

from openai import OpenAI


def incident_summary(log_findings: list[dict], model: str = "gpt-4.1-mini") -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = {
        "task": "incident_review_summary",
        "logs": log_findings,
    }
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Summarize operational error logs into a concise incident review.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    return {"provider": "OpenAI", "model": model, "summary": response.output_text}
