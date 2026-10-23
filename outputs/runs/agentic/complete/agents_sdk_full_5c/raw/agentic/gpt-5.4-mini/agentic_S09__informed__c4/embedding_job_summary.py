from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from openai import OpenAI

from embeddings_client import get_chat_model, get_openai_client


@dataclass(frozen=True)
class EmbeddingJobSummary:
    title: str
    summary: str


def embedding_job_summary(job_name: str, completed: int, failed: int, notes: Iterable[str]) -> EmbeddingJobSummary:
    client: OpenAI = get_openai_client()
    model = get_chat_model()
    prompt = "\n".join([
        f"Job: {job_name}",
        f"Completed: {completed}",
        f"Failed: {failed}",
        "Notes:",
        *[f"- {note}" for note in notes],
    ])
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize embedding pipeline results concisely."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return EmbeddingJobSummary(title=job_name, summary=response.choices[0].message.content or "")
