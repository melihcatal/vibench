from __future__ import annotations

import json
import os
from typing import Any, Iterable

from openai import OpenAI


OPENAI_SUMMARY_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def _summary_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI job summarization")
    return OpenAI(api_key=api_key, base_url=os.getenv("OPENAI_BASE_URL"))


def summarize_embedding_job(job_rows: Iterable[dict[str, Any]], *, model: str = OPENAI_SUMMARY_MODEL) -> str:
    rows = list(job_rows)
    client = _summary_client()
    prompt = {
        "task": "Summarize an embeddings batch job for operators.",
        "rows": rows,
        "fields_to_cover": ["document_count", "errors", "avg_latency_ms", "token_usage", "quality_flags"],
    }
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You summarize vector embedding pipeline runs concisely and accurately."},
            {"role": "user", "content": json.dumps(prompt)},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
