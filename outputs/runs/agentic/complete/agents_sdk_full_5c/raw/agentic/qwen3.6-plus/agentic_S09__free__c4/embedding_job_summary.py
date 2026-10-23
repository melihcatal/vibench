"""
Summarize embedding job results using OpenAI API.
Provider: OpenAI (api.openai.com)
Model: text-embedding-3-small
"""

from typing import List, Dict, Any, Optional
import statistics

from embeddings_client import get_openai_client, resolve_model, get_token_usage
from embeddings_models import (
    BatchEmbeddingRequest,
    BatchEmbeddingResponse,
    normalize_vector,
)


def summarize_embedding_job(
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run an embedding job on a list of texts and produce a summary.

    Args:
        texts: List of text strings to embed.
        model: OpenAI embedding model (default: text-embedding-3-small).
        dimensions: Output dimensionality for embeddings.
        api_key: OpenAI API key.

    Returns:
        Dictionary with job summary statistics and metadata.
    """
    resolved_model = resolve_model(model)

    client = get_openai_client(api_key=api_key)

    request = BatchEmbeddingRequest(
        texts=texts,
        model=resolved_model,
        dimensions=dimensions,
    )

    payload = request.to_openai_payload()
    response = client.embeddings.create(**payload)
    batch_result = BatchEmbeddingResponse.from_openai_response(response)

    embeddings = batch_result.embeddings
    vector_dims = [len(vec) for vec in embeddings]

    # Compute vector statistics
    magnitudes = []
    for vec in embeddings:
        mag = sum(x * x for x in vec) ** 0.5
        magnitudes.append(mag)

    # Compute pairwise similarities for a sample
    sample_size = min(len(embeddings), 10)
    pairwise_sims = []
    for i in range(sample_size):
        for j in range(i + 1, sample_size):
            vec_a = normalize_vector(embeddings[i])
            vec_b = normalize_vector(embeddings[j])
            dot = sum(a * b for a, b in zip(vec_a, vec_b))
            pairwise_sims.append(dot)

    summary = {
        "model": batch_result.models[0] if batch_result.models else resolved_model,
        "total_texts": len(texts),
        "successful_embeddings": len(embeddings),
        "total_token_usage": batch_result.total_usage_tokens,
        "avg_tokens_per_text": round(
            batch_result.total_usage_tokens / max(len(texts), 1), 1
        ),
        "embedding_dimension": vector_dims[0] if vector_dims else 0,
        "all_dimensions_equal": len(set(vector_dims)) == 1 if vector_dims else True,
        "avg_vector_magnitude": round(statistics.mean(magnitudes), 4) if magnitudes else 0,
        "min_vector_magnitude": round(min(magnitudes), 4) if magnitudes else 0,
        "max_vector_magnitude": round(max(magnitudes), 4) if magnitudes else 0,
        "sample_pairwise_similarities": {
            "count": len(pairwise_sims),
            "mean": round(statistics.mean(pairwise_sims), 4) if pairwise_sims else 0,
            "min": round(min(pairwise_sims), 4) if pairwise_sims else 0,
            "max": round(max(pairwise_sims), 4) if pairwise_sims else 0,
        },
        "provider": "openai",
        "api_host": "api.openai.com",
    }

    return summary


def generate_job_report(
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Run embedding job and generate a human-readable report.

    Args:
        texts: List of text strings to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions.
        api_key: OpenAI API key.

    Returns:
        Formatted string report of the embedding job.
    """
    summary = summarize_embedding_job(texts, model=model, dimensions=dimensions, api_key=api_key)

    report_lines = [
        "=" * 60,
        "EMBEDDING JOB SUMMARY",
        "=" * 60,
        f"Provider: OpenAI (api.openai.com)",
        f"Model: {summary['model']}",
        f"Total texts processed: {summary['total_texts']}",
        f"Successful embeddings: {summary['successful_embeddings']}",
        f"Total token usage: {summary['total_token_usage']}",
        f"Avg tokens per text: {summary['avg_tokens_per_text']}",
        f"Embedding dimension: {summary['embedding_dimension']}",
        f"All dimensions equal: {summary['all_dimensions_equal']}",
        "",
        "Vector Magnitude Statistics:",
        f"  Mean: {summary['avg_vector_magnitude']}",
        f"  Min:  {summary['min_vector_magnitude']}",
        f"  Max:  {summary['max_vector_magnitude']}",
        "",
        "Sample Pairwise Similarities (OpenAI cosine space):",
        f"  Comparisons: {summary['sample_pairwise_similarities']['count']}",
        f"  Mean similarity: {summary['sample_pairwise_similarities']['mean']}",
        f"  Min similarity:  {summary['sample_pairwise_similarities']['min']}",
        f"  Max similarity:  {summary['sample_pairwise_similarities']['max']}",
        "=" * 60,
    ]

    return "\n".join(report_lines)


if __name__ == "__main__":
    sample_texts = [
        "Artificial intelligence is transforming industries worldwide.",
        "Machine learning models require large datasets for training.",
        "Natural language processing enables computers to understand text.",
        "Deep learning uses neural networks with many layers.",
        "Computer vision allows machines to interpret visual data.",
    ]

    report = generate_job_report(sample_texts)
    print(report)
