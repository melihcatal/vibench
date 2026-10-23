from __future__ import annotations

import os

import requests


OPENAI_RESPONSES_MODEL = os.getenv("OPENAI_RESPONSES_MODEL", "gpt-4.1-mini")


def embedding_job_summary(job_results: list[dict[str, object]]) -> dict[str, object]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    payload = {
        "model": OPENAI_RESPONSES_MODEL,
        "input": [
            {
                "role": "system",
                "content": "Summarize embedding pipeline results with totals, failures, and notable anomalies.",
            },
            {
                "role": "user",
                "content": str(job_results),
            },
        ],
    }
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30.0,
    )
    response.raise_for_status()
    body = response.json()
    summary = body.get("output_text", "")
    return {
        "provider": "openai",
        "model": OPENAI_RESPONSES_MODEL,
        "summary": summary,
        "raw": body,
    }
