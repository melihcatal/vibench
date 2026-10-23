"""
[LATER-STEP] Summarize embedding job results.
Provider: OpenAI embeddings API (api.openai.com, model text-embedding-3-small).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from embeddings_client import configure_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse, EmbeddingResult


@dataclass
class JobSummary:
    """Summary statistics for an embedding job."""
    total_texts: int
    total_tokens_used: int
    embedding_dimension: int
    avg_vector_magnitude: float
    model_used: str
    results: list[EmbeddingResult]


def embedding_job_summary(
    texts: list[str],
    model: str = "text-embedding-3-small",
    api_key: str | None = None,
) -> JobSummary:
    """
    Generate embeddings for a batch of texts and return a summary
    of the embedding job using the OpenAI embeddings API
    (api.openai.com, model text-embedding-3-small).

    Args:
        texts: List of text strings to embed.
        model: OpenAI model identifier.
        api_key: OpenAI API key.

    Returns:
        JobSummary with statistics and embedding results.
    """
    client, _ = configure_client(api_key=api_key)

    request = EmbeddingRequest(input_texts=texts, model=model)
    raw_response = client.embeddings.create(**request.to_openai_kwargs())
    response = EmbeddingResponse.from_openai_response(raw_response, texts)

    total_texts = len(response.results)
    embedding_dimension = len(response.results[0].vector) if response.results else 0

    magnitudes = []
    for result in response.results:
        mag = math.sqrt(sum(v * v for v in result.vector))
        magnitudes.append(mag)
        result.usage_tokens = 0

    avg_magnitude = sum(magnitudes) / len(magnitudes) if magnitudes else 0.0

    return JobSummary(
        total_texts=total_texts,
        total_tokens_used=response.total_tokens,
        embedding_dimension=embedding_dimension,
        avg_vector_magnitude=round(avg_magnitude, 4),
        model_used=response.model,
        results=response.results,
    )


if __name__ == "__main__":
    sample_texts = [
        "Natural language processing enables machines to understand text.",
        "Deep learning models have revolutionized AI capabilities.",
        "Vector databases store high-dimensional embeddings efficiently.",
        "Semantic search finds relevant documents by meaning.",
    ]
    summary = embedding_job_summary(sample_texts)
    print(f"Model: {summary.model_used}")
    print(f"Texts embedded: {summary.total_texts}")
    print(f"Tokens used: {summary.total_tokens_used}")
    print(f"Embedding dimension: {summary.embedding_dimension}")
    print(f"Avg vector magnitude: {summary.avg_vector_magnitude}")
