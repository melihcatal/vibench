from __future__ import annotations

import json
import os
from typing import Any, Mapping, Sequence

from openai import OpenAI


def _client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required for GPT summaries")
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def summarize_embedding_job(
    job_name: str,
    total_items: int,
    succeeded: int,
    failed: int,
    sample_errors: Sequence[str] | None = None,
    usage: Mapping[str, Any] | None = None,
    model: str = "gpt-4o-mini",
) -> str:
    payload = {
        "job_name": job_name,
        "total_items": total_items,
        "succeeded": succeeded,
        "failed": failed,
        "sample_errors": list(sample_errors or []),
        "usage": dict(usage or {}),
    }
    client = _client()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Summarize embedding pipeline results concisely for operators, calling out completion rate, failure patterns, and next actions.",
            },
            {
                "role": "user",
                "content": json.dumps(payload, ensure_ascii=False),
            },
        ],
    )
    return response.output_text.strip()
