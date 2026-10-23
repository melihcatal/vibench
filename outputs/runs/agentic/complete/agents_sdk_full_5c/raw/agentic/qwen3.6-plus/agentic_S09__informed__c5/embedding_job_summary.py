"""
[LATER-STEP] Summarize embedding job results.
Provider: OpenAI GPT-4 via Chat Completions API
SDK: openai
Auth: OPENAI_API_KEY
"""

from __future__ import annotations

import json
from typing import List, Optional, Dict

from openai import OpenAI
from embeddings_models import EmbeddingBatchResponse


OPENAI_CHAT_MODEL = "gpt-4o-mini"


def summarize_embedding_job(
    batch_response: EmbeddingBatchResponse,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    include_stats: bool = True,
) -> str:
    """
    Summarize the results of an embedding job using OpenAI GPT-4.

    Takes an EmbeddingBatchResponse (produced by embed_batch) and generates
    a natural-language summary describing the job outcome, including token
    usage, number of embeddings, and any notable observations.

    Args:
        batch_response: The EmbeddingBatchResponse from a prior embedding call.
        api_key: Optional OpenAI API key (falls back to OPENAI_API_KEY env var).
        model: OpenAI chat model identifier (default: gpt-4o-mini).
        include_stats: Whether to include usage statistics in the summary.

    Returns:
        A string summary of the embedding job.
    """
    import os

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required for OpenAI GPT-4 chat completions.")

    client = OpenAI(api_key=key)
    chat_model = model or OPENAI_CHAT_MODEL

    num_results = len(batch_response.results)
    vectors = batch_response.results
    vector_lengths = set(len(r.vector) for r in vectors) if vectors else {0}
    text_lengths = [len(r.text) for r in vectors]

    stats_section = ""
    if include_stats:
        stats_section = (
            f"Token usage: {batch_response.total_tokens} tokens.\n"
            f"Embedding model: {batch_response.model}.\n"
            f"Vector dimensionalities observed: {sorted(vector_lengths)}.\n"
            f"Input text length range: {min(text_lengths)}-{max(text_lengths)} chars.\n"
        )

    prompt = (
        f"Summarize the following embedding job results:\n"
        f"Total embeddings generated: {num_results}\n"
        f"Model used: {batch_response.model}\n"
        f"Total tokens consumed: {batch_response.total_tokens}\n"
        f"Unique vector sizes: {sorted(vector_lengths)}\n"
        f"\n"
        f"Provide a concise summary of the job outcome, including any observations "
        f"about the data processed and efficiency of the embedding operation."
    )

    response = client.chat.completions.create(
        model=chat_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes embedding job results."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    summary_text = response.choices[0].message.content or ""

    if include_stats:
        summary_text = f"{stats_section}\n{summary_text}"

    return summary_text


def summarize_embedding_job_json(
    batch_response: EmbeddingBatchResponse,
    api_key: Optional[str] = None,
) -> Dict:
    """
    Return a structured JSON summary of an embedding job.

    Args:
        batch_response: The EmbeddingBatchResponse to summarize.
        api_key: Optional OpenAI API key.

    Returns:
        Dictionary with job summary fields.
    """
    vectors = batch_response.results
    vector_lengths = [len(r.vector) for r in vectors] if vectors else []

    return {
        "model": batch_response.model,
        "total_embeddings": len(vectors),
        "total_tokens": batch_response.total_tokens,
        "vector_dimensions": list(set(vector_lengths)),
        "avg_vector_dim": sum(vector_lengths) / len(vector_lengths) if vector_lengths else 0,
        "provider": "OpenAI Embeddings API",
        "host": "api.openai.com",
    }


if __name__ == "__main__":
    from embed_batch import embed_batch

    sample_texts = [
        "OpenAI provides state-of-the-art language models.",
        "Embedding models convert text to dense vectors.",
        "Semantic search relies on vector similarity.",
    ]
    batch_resp = embed_batch(sample_texts)
    summary = summarize_embedding_job(batch_resp)
    print(summary)
