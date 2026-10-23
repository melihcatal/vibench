from __future__ import annotations

import os

from openai import OpenAI


DEFAULT_SUMMARY_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_embedding_job(
    job_result: dict, model: str = DEFAULT_SUMMARY_MODEL
) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Summarize embedding job outcomes with counts, issues, and readiness in concise operational language.",
            },
            {
                "role": "user",
                "content": f"Embedding job result: {job_result}",
            },
        ],
    )
    return response.output_text.strip()
