from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


def summarize_embedding_job(
    job_result: dict[str, Any], model: str | None = None
) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    selected_model = model or os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")
    response = client.responses.create(
        model=selected_model,
        input=[
            {
                "role": "system",
                "content": "Summarize embedding pipeline results with operational clarity.",
            },
            {
                "role": "user",
                "content": f"Summarize this embedding job result: {job_result}",
            },
        ],
    )
    return {
        "provider": "openai",
        "model": selected_model,
        "summary": response.output_text,
    }
