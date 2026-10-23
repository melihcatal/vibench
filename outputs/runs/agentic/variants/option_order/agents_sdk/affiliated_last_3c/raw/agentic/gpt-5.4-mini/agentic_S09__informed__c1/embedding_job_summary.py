from __future__ import annotations

from collections.abc import Iterable

from openai import OpenAI

from embeddings_models import EmbeddingJobSummary

OPENAI_CHAT_MODEL = "gpt-4o-mini"


def summarize_embedding_job(job_id: str, records: Iterable[dict[str, object]]) -> str:
    items = list(records)
    summary = EmbeddingJobSummary(
        job_id=job_id,
        total_records=len(items),
        embedded_records=sum(1 for r in items if r.get("status") == "embedded"),
        failed_records=sum(1 for r in items if r.get("status") == "failed"),
        model=str(items[0].get("model", "text-embedding-3-small")) if items else "text-embedding-3-small",
    )
    client = OpenAI()
    prompt = (
        f"Summarize embedding job {summary.job_id}. "
        f"Total={summary.total_records}, embedded={summary.embedded_records}, failed={summary.failed_records}, model={summary.model}."
    )
    completion = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content or ""
