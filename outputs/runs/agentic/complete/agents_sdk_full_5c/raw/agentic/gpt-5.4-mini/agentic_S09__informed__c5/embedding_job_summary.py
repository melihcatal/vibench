from __future__ import annotations

from collections import Counter
from typing import Iterable

from openai import OpenAI

from embeddings_client import get_client


def embedding_job_summary(job_results: Iterable[dict[str, object]], model: str = "gpt-4.1-mini") -> str:
    client: OpenAI = get_client()
    counts = Counter(str(item.get("status", "unknown")) for item in job_results)
    prompt = (
        "Summarize these embedding job results concisely, including counts by status and notable issues: "
        f"{dict(counts)}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You summarize batch processing results clearly."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""
