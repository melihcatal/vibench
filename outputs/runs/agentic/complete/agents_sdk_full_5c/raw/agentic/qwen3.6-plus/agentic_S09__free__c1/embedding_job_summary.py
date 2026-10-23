"""Summarize embedding job results using OpenAI embeddings API metadata."""

import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import numpy as np
from openai import OpenAI

from embeddings_client import get_openai_client, get_model_info
from embeddings_models import EmbeddingResponse, normalize_vector
from embed_batch import embed_batch


@dataclass
class EmbeddingJobSummary:
    """Summary statistics for an embedding job."""
    total_texts: int
    model: str
    total_tokens: int
    avg_tokens_per_text: float
    vector_dimension: int
    avg_vector_norm: float
    vector_variance: float
    processing_details: Dict[str, Any] = field(default_factory=dict)


def summarize_embedding_job(
    texts: List[str],
    model: str = "text-embedding-3-small",
) -> EmbeddingJobSummary:
    """Run an embedding job on texts and return a summary.

    Uses OpenAI's text-embedding-3-small model. Summarizes token usage,
    vector statistics, and embedding quality metrics.

    Args:
        texts: List of texts to embed and analyze.
        model: OpenAI embedding model identifier.

    Returns:
        EmbeddingJobSummary with job statistics.
    """
    client = get_openai_client()
    model_info = get_model_info(model)

    # Run the embedding job
    batch_response = embed_batch(texts, model=model)

    # Compute vector statistics
    vectors_array = batch_response.to_numpy_array()
    vector_norms = np.linalg.norm(vectors_array, axis=1)
    avg_norm = float(np.mean(vector_norms))
    vector_variance = float(np.mean(np.var(vectors_array, axis=0)))

    # Compute token statistics
    total_tokens = batch_response.total_tokens
    avg_tokens = total_tokens / len(texts) if texts else 0.0

    return EmbeddingJobSummary(
        total_texts=len(texts),
        model=model,
        total_tokens=total_tokens,
        avg_tokens_per_text=avg_tokens,
        vector_dimension=vectors_array.shape[1],
        avg_vector_norm=avg_norm,
        vector_variance=vector_variance,
        processing_details={
            "expected_dimension": model_info.get("dimensions"),
            "max_input_tokens": model_info.get("max_input_tokens"),
            "api_endpoint": "https://api.openai.com/v1/embeddings",
        },
    )


def get_embedding_quality_report(
    texts: List[str],
    model: str = "text-embedding-3-small",
) -> Dict[str, Any]:
    """Generate a quality report for embeddings of the given texts.

    Uses OpenAI embeddings to analyze distribution and detect anomalies.

    Args:
        texts: Texts to analyze.
        model: OpenAI embedding model.

    Returns:
        Dictionary with quality metrics.
    """
    summary = summarize_embedding_job(texts, model=model)

    vectors = embed_batch(texts, model=model).to_numpy_array()

    # Compute pairwise similarities to find outliers
    normalized_vectors = np.array([
        normalize_vector(v) for v in vectors
    ])

    # Self-similarity matrix (diagonal is 1.0)
    similarity_matrix = normalized_vectors @ normalized_vectors.T

    # Average similarity to other texts
    avg_similarities = []
    for i in range(len(texts)):
        sims = similarity_matrix[i]
        other_sims = np.concatenate([sims[:i], sims[i+1:]])
        avg_similarities.append(float(np.mean(other_sims)))

    return {
        "job_summary": {
            "total_texts": summary.total_texts,
            "model": summary.model,
            "total_tokens": summary.total_tokens,
            "avg_tokens_per_text": summary.avg_tokens_per_text,
            "vector_dimension": summary.vector_dimension,
        },
        "quality_metrics": {
            "avg_vector_norm": summary.avg_vector_norm,
            "vector_variance": summary.vector_variance,
            "avg_inter_text_similarity": float(np.mean(avg_similarities)),
            "min_avg_similarity": float(np.min(avg_similarities)),
            "max_avg_similarity": float(np.max(avg_similarities)),
        },
        "provider": "OpenAI",
        "api_endpoint": "https://api.openai.com/v1/embeddings",
    }


def compare_models_on_corpus(
    texts: List[str],
    models: List[str] = None,
) -> Dict[str, EmbeddingJobSummary]:
    """Compare embedding performance across multiple OpenAI models."""
    if models is None:
        models = ["text-embedding-3-small", "text-embedding-3-large"]

    results = {}
    for model in models:
        summary = summarize_embedding_job(texts, model=model)
        results[model] = summary

    return results


if __name__ == "__main__":
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning models learn patterns from data.",
        "Embeddings represent text as dense vectors.",
        "OpenAI provides powerful language models.",
        "Natural language processing is a growing field.",
    ]

    summary = summarize_embedding_job(sample_texts)
    print(f"Model: {summary.model}")
    print(f"Total texts: {summary.total_texts}")
    print(f"Total tokens: {summary.total_tokens}")
    print(f"Avg tokens/text: {summary.avg_tokens_per_text:.1f}")
    print(f"Vector dimension: {summary.vector_dimension}")
    print(f"Avg vector norm: {summary.avg_vector_norm:.4f}")

    report = get_embedding_quality_report(sample_texts)
    print(f"\nQuality Report:")
    print(f"  Avg inter-text similarity: {report['quality_metrics']['avg_inter_text_similarity']:.4f}")
