from __future__ import annotations

import os
from typing import Any

import requests


def embedding_job_summary(job_results: list[dict[str, Any]]) -> dict[str, Any]:
    endpoint = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    prompt = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "Summarize embedding pipeline results concisely with totals, failures, and recommendations.",
            },
            {"role": "user", "content": str(job_results)},
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=prompt,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    message = data["choices"][0]["message"]["content"]
    total = len(job_results)
    failures = sum(1 for item in job_results if not item.get("success", True))
    return {
        "provider": "OpenAI",
        "model": "gpt-4o-mini",
        "job_count": total,
        "failed_jobs": failures,
        "summary": message,
    }
