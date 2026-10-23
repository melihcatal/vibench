"""
embedding_job_summary.py - Summarize embedding job results.

Provider: OpenAI Chat Completions API
Model: gpt-4o-mini
SDK: openai
Auth: OPENAI_API_KEY
"""

import json
import os
from typing import Any

from openai import OpenAI


OPENAI_CHAT_MODEL = "gpt-4o-mini"

_api_key = os.environ.get("OPENAI_API_KEY", "")


def _get_chat_client() -> OpenAI:
    if not _api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    return OpenAI(api_key=_api_key)


def summarize_embedding_job(
    job_metadata: dict[str, Any],
    result_stats: dict[str, Any],
) -> str:
    """Generate a human-readable summary of an embedding job via OpenAI GPT-4o-mini.

    Args:
        job_metadata: Metadata about the embedding job (model, input count, etc.).
        result_stats: Statistics about the results (token usage, dimensions, etc.).

    Returns:
        A formatted text summary of the embedding job.
    """
    client = _get_chat_client()

    prompt = (
        "You are an AI assistant that summarizes embedding job results. "
        "Write a concise, professional summary based on the following metadata:\n\n"
        f"Job metadata: {json.dumps(job_metadata, indent=2)}\n\n"
        f"Result statistics: {json.dumps(result_stats, indent=2)}\n\n"
        "Include: model used, total documents processed, token consumption, "
        "average vector dimensionality, and any notable observations."
    )

    response = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You summarize ML embedding pipeline jobs."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    summary = response.choices[0].message.content or "No summary generated."
    return summary


def build_summary_from_results(
    texts_embedded: list[str],
    embedding_model: str,
    vector_dimension: int,
    total_tokens: int,
) -> str:
    """Convenience wrapper that constructs metadata from raw results and summarizes.

    Uses OpenAI gpt-4o-mini to produce the narrative summary.

    Args:
        texts_embedded: The original texts that were embedded.
        embedding_model: The embedding model identifier used.
        vector_dimension: Dimensionality of the output vectors.
        total_tokens: Total token usage for the embedding job.

    Returns:
        A formatted summary string.
    """
    metadata = {
        "embedding_model": embedding_model,
        "provider": "OpenAI",
        "document_count": len(texts_embedded),
        "avg_text_length": sum(len(t) for t in texts_embedded) / max(len(texts_embedded), 1),
    }
    stats = {
        "vector_dimension": vector_dimension,
        "total_tokens": total_tokens,
        "tokens_per_doc": total_tokens / max(len(texts_embedded), 1),
    }
    return summarize_embedding_job(metadata, stats)


def main() -> None:
    sample_texts = [
        "Neural networks learn hierarchical representations from data.",
        "Gradient descent optimizes model parameters iteratively.",
        "Transformers use self-attention for sequence modeling.",
    ]
    summary = build_summary_from_results(
        texts_embedded=sample_texts,
        embedding_model="text-embedding-3-small",
        vector_dimension=1536,
        total_tokens=30,
    )
    print(summary)


if __name__ == "__main__":
    main()
