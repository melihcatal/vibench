from __future__ import annotations

import os
from collections.abc import Sequence

from openai import OpenAI


def summarize_embedding_job(
    *,
    total_items: int,
    embedded_items: int,
    failed_items: int,
    model_name: str,
    duration_seconds: float,
    sample_errors: Sequence[str] | None = None,
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    errors = "\n".join(f"- {item}" for item in (sample_errors or [])) or "- None"
    prompt = (
        "Summarize this embedding pipeline run for an operator in 4 concise bullet points. "
        "Mention completion rate, failures, likely causes, and a next action.\n\n"
        f"Embedding model: {model_name}\n"
        f"Total items: {total_items}\n"
        f"Embedded items: {embedded_items}\n"
        f"Failed items: {failed_items}\n"
        f"Duration seconds: {duration_seconds:.2f}\n"
        f"Sample errors:\n{errors}"
    )
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "You produce concise operational summaries."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
