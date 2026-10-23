"""
Later-step: Summarize embedding job results.
Provider: OpenAI GPT-4o via openai SDK for summarization.
Auth: OPENAI_API_KEY
Model: gpt-4o
"""

import json
from typing import List, Optional

from openai import OpenAI

from embeddings_client import create_embeddings_client


def summarize_embedding_job(
    job_metadata: dict,
    embedding_stats: dict,
    sample_queries: Optional[List[str]] = None,
    model: str = "gpt-4o",
    api_key: Optional[str] = None,
) -> str:
    """Summarize the results of an embedding job using OpenAI GPT-4o.

    Args:
        job_metadata: Metadata about the embedding job (timestamps, model used, etc.).
        embedding_stats: Statistics about the embeddings (avg token count, dimensionality, etc.).
        sample_queries: Optional sample texts that were embedded.
        model: OpenAI chat model for summarization (default: gpt-4o).
        api_key: Optional override for OPENAI_API_KEY.

    Returns:
        A human-readable summary of the embedding job.
    """
    client = create_embeddings_client(api_key=api_key)

    payload = {
        "job_metadata": job_metadata,
        "embedding_stats": embedding_stats,
        "sample_queries": sample_queries or [],
    }

    system_prompt = (
        "You are an AI assistant that summarizes embedding job results. "
        "Provide a concise, professional summary including key metrics, "
        "data quality observations, and any notable patterns."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Summarize this embedding job:\n{json.dumps(payload, indent=2)}",
        },
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        max_tokens=500,
    )

    summary = response.choices[0].message.content or ""
    return summary


if __name__ == "__main__":
    meta = {
        "job_id": "emb-job-001",
        "model": "text-embedding-3-small",
        "total_texts": 15000,
        "start_time": "2025-01-15T08:00:00Z",
        "end_time": "2025-01-15T08:12:34Z",
    }
    stats = {
        "avg_tokens_per_text": 45,
        "total_tokens": 675000,
        "embedding_dimension": 1536,
        "success_rate": 0.998,
    }
    samples = [
        "How to integrate OpenAI embeddings into a Python app",
        "Best practices for semantic search with vector databases",
    ]
    summary = summarize_embedding_job(meta, stats, samples)
    print(summary)
