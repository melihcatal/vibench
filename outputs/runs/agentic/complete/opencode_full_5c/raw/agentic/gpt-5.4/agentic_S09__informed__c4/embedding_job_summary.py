from __future__ import annotations

import os
from typing import Any

from openai import OpenAI


def embedding_job_summary(
    job_result: dict[str, Any], model: str = "gpt-4o-mini"
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {
        "status": job_result.get("status"),
        "model": job_result.get("model"),
        "input_count": job_result.get("input_count"),
        "completed_count": job_result.get("completed_count"),
        "error_count": job_result.get("error_count"),
        "duration_seconds": job_result.get("duration_seconds"),
    }
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You summarize embedding job outcomes clearly and tersely.",
            },
            {
                "role": "user",
                "content": f"Summarize this embedding job result: {prompt}",
            },
        ],
    )
    return response.output_text.strip()
