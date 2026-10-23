"""
Summarize embedding job results.

Provider: OpenAI Embeddings API (https://api.openai.com)
Model: text-embedding-3-small
"""

from typing import List, Optional, Dict, Any

from embeddings_client import (
    get_openai_client,
    load_embeddings_config,
    build_embeddings_payload,
    parse_embeddings_response,
)
from embeddings_models import EmbeddingRequest, EmbeddingResponse


class EmbeddingJobSummary:
    """
    Summary of an embedding job processed via OpenAI's API.

    Attributes:
        total_texts: Total number of texts processed
        successful: Number of successful embeddings
        failed: Number of failed embeddings
        total_tokens: Total token usage
        model: OpenAI model used
        avg_dimension: Average embedding dimension
    """

    def __init__(
        self,
        total_texts: int = 0,
        successful: int = 0,
        failed: int = 0,
        total_tokens: int = 0,
        model: str = "text-embedding-3-small",
        avg_dimension: int = 0,
        embedding_stats: Optional[Dict[str, Any]] = None,
    ):
        self.total_texts = total_texts
        self.successful = successful
        self.failed = failed
        self.total_tokens = total_tokens
        self.model = model
        self.avg_dimension = avg_dimension
        self.embedding_stats = embedding_stats or {}

    @property
    def success_rate(self) -> float:
        if self.total_texts == 0:
            return 0.0
        return self.successful / self.total_texts

    @property
    def tokens_per_text(self) -> float:
        if self.successful == 0:
            return 0.0
        return self.total_tokens / self.successful

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_texts": self.total_texts,
            "successful": self.successful,
            "failed": self.failed,
            "success_rate": round(self.success_rate, 4),
            "total_tokens": self.total_tokens,
            "tokens_per_text": round(self.tokens_per_text, 2),
            "model": self.model,
            "avg_dimension": self.avg_dimension,
            "embedding_stats": self.embedding_stats,
        }


def run_embedding_job(
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    batch_size: int = 100,
) -> EmbeddingJobSummary:
    """
    Run an embedding job on a list of texts and produce a summary.

    Processes texts in batches via OpenAI's embeddings API, tracking
    successes, failures, and token usage.

    Args:
        texts: List of texts to embed
        model: OpenAI embedding model (default: text-embedding-3-small)
        dimensions: Optional embedding dimensionality
        api_key: OpenAI API key
        batch_size: Texts per API call

    Returns:
        EmbeddingJobSummary with job statistics
    """
    if not texts:
        return EmbeddingJobSummary()

    config = load_embeddings_config()
    target_model = model or config["model"]
    target_dimensions = dimensions or config["dimensions"]

    client = get_openai_client(api_key=api_key)

    total_texts = len(texts)
    successful = 0
    failed = 0
    total_tokens = 0
    all_embeddings: List[List[float]] = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        valid_batch = [t for t in batch if t and t.strip()]

        if not valid_batch:
            failed += len(batch)
            continue

        try:
            payload = build_embeddings_payload(
                texts=valid_batch,
                model=target_model,
                dimensions=target_dimensions,
            )
            response = client.embeddings.create(**payload)
            embeddings = parse_embeddings_response(response)
            all_embeddings.extend(embeddings)
            successful += len(valid_batch)
            total_tokens += response.usage.total_tokens
        except Exception:
            failed += len(valid_batch)

    failed += (total_texts - successful - failed)

    avg_dimension = 0
    if all_embeddings:
        avg_dimension = len(all_embeddings[0])

    summary = EmbeddingJobSummary(
        total_texts=total_texts,
        successful=successful,
        failed=failed,
        total_tokens=total_tokens,
        model=target_model,
        avg_dimension=avg_dimension,
        embedding_stats={
            "embedding_count": len(all_embeddings),
        },
    )

    return summary


def summarize_embeddings(
    embeddings: List[List[float]],
) -> Dict[str, Any]:
    """
    Compute summary statistics for a list of embedding vectors.

    Args:
        embeddings: List of embedding vectors from OpenAI API

    Returns:
        Dict with mean, variance, and norm statistics
    """
    if not embeddings:
        return {}

    dimensions = len(embeddings[0])
    means = []
    norms = []

    for d in range(dimensions):
        col_sum = sum(emb[d] for emb in embeddings)
        means.append(col_sum / len(embeddings))

    for emb in embeddings:
        norm = sum(x * x for x in emb) ** 0.5
        norms.append(norm)

    return {
        "dimensions": dimensions,
        "count": len(embeddings),
        "mean_magnitude": sum(means) / len(means) if means else 0,
        "avg_norm": sum(norms) / len(norms) if norms else 0,
        "max_norm": max(norms) if norms else 0,
        "min_norm": min(norms) if norms else 0,
    }


if __name__ == "__main__":
    import json

    sample_texts = [
        "OpenAI provides advanced AI models.",
        "Embeddings capture semantic meaning.",
        "Text similarity enables search.",
    ]
    summary = run_embedding_job(sample_texts)
    print(json.dumps(summary.to_dict(), indent=2))
