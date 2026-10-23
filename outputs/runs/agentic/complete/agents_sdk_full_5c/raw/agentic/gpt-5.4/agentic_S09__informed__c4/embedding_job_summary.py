from __future__ import annotations

import json
import os
from typing import Any, Mapping, Sequence

from openai import OpenAI


OPENAI_CHAT_MODEL = "gpt-4o-mini"


def _client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required for OpenAI chat completions")
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def summarize_embedding_job(
    job_name: str,
    total_items: int,
    embedded_items: int,
    failed_items: int,
    sample_errors: Sequence[str] | None = None,
    usage: Mapping[str, Any] | None = None,
    *,
    model: str = OPENAI_CHAT_MODEL,
) -> str:
    payload = {
        "job_name": job_name,
        "total_items": total_items,
        "embedded_items": embedded_items,
        "failed_items": failed_items,
        "sample_errors": list(sample_errors or []),
        "usage": dict(usage or {}),
    }
    client = _client()
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You summarize embedding pipeline job results for operators in concise prose.",
            },
            {
                "role": "user",
                "content": "Summarize this embedding job result and mention completion rate, failures, and any operational concern: " + json.dumps(payload),
            },
        ],
    )
    return response.choices[0].message.content or ""
