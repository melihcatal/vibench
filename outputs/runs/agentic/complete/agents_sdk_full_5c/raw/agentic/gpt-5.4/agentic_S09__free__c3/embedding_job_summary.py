from __future__ import annotations

from collections.abc import Sequence

from anthropic import Anthropic

from embeddings_models import summarize_embedding_lengths


def embedding_job_summary(job_name: str, source_count: int, vectors: Sequence[Sequence[float]], failed_items: Sequence[str] | None = None) -> dict:
    failed_items = list(failed_items or [])
    stats = summarize_embedding_lengths(vectors)
    client = Anthropic()
    prompt = (
        f"Summarize an embedding pipeline job named {job_name!r}. "
        f"Source items: {source_count}. Successful embeddings: {stats['count']}. "
        f"Vector length min/max/avg: {stats['min']}/{stats['max']}/{stats['avg']:.1f}. "
        f"Failures: {len(failed_items)}. Failed item ids: {failed_items[:10]}. "
        "Produce a concise operational summary with quality signals and follow-up recommendations."
    )
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=220,
        messages=[{"role": "user", "content": prompt}],
    )
    summary_text = "".join(block.text for block in response.content if getattr(block, "type", "") == "text")
    return {
        "provider": "anthropic",
        "model": "claude-3-5-sonnet-20241022",
        "job": job_name,
        "stats": stats,
        "summary": summary_text,
    }
