"""
Computes cosine similarity between two embedded texts using OpenAI API.
Provider: OpenAI (api.openai.com)
Model: text-embedding-3-small
"""

import sys
from typing import Optional, Tuple

from embeddings_client import get_openai_client, resolve_model
from embeddings_models import (
    BatchEmbeddingRequest,
    BatchEmbeddingResponse,
    cosine_similarity,
    normalize_vector,
)


def compute_similarity(
    text_a: str,
    text_b: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    normalize: bool = True,
    api_key: Optional[str] = None,
) -> Tuple[float, float, float]:
    """
    Compute cosine similarity between two text strings using OpenAI embeddings.

    Args:
        text_a: First text string.
        text_b: Second text string.
        model: OpenAI embedding model (default: text-embedding-3-small).
        dimensions: Output dimensionality for embeddings.
        normalize: Whether to L2-normalize vectors before computing similarity.
        api_key: OpenAI API key.

    Returns:
        Tuple of (cosine_similarity_score, raw_dot_product, vector_a_magnitude).
    """
    resolved_model = resolve_model(model)

    client = get_openai_client(api_key=api_key)

    request = BatchEmbeddingRequest(
        texts=[text_a, text_b],
        model=resolved_model,
        dimensions=dimensions,
    )

    payload = request.to_openai_payload()
    response = client.embeddings.create(**payload)
    batch_result = BatchEmbeddingResponse.from_openai_response(response)

    vec_a = batch_result.embeddings[0]
    vec_b = batch_result.embeddings[1]

    if normalize:
        vec_a = normalize_vector(vec_a)
        vec_b = normalize_vector(vec_b)

    sim_score = cosine_similarity(vec_a, vec_b)

    import math
    magnitude_a = math.sqrt(sum(x * x for x in batch_result.embeddings[0]))

    return sim_score, sim_score, magnitude_a


def get_similarity_with_usage(
    text_a: str,
    text_b: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> dict:
    """
    Compute cosine similarity and return detailed results including token usage.

    Args:
        text_a: First text string.
        text_b: Second text string.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions.
        api_key: OpenAI API key.

    Returns:
        Dictionary with similarity_score, token_usage, model, and vectors.
    """
    resolved_model = resolve_model(model)

    client = get_openai_client(api_key=api_key)

    request = BatchEmbeddingRequest(
        texts=[text_a, text_b],
        model=resolved_model,
        dimensions=dimensions,
    )

    payload = request.to_openai_payload()
    response = client.embeddings.create(**payload)
    batch_result = BatchEmbeddingResponse.from_openai_response(response)

    vec_a = normalize_vector(batch_result.embeddings[0])
    vec_b = normalize_vector(batch_result.embeddings[1])

    sim_score = cosine_similarity(vec_a, vec_b)

    return {
        "similarity_score": sim_score,
        "token_usage": batch_result.total_usage_tokens,
        "model": batch_result.models[0],
        "vector_a_dimensions": len(batch_result.embeddings[0]),
        "vector_b_dimensions": len(batch_result.embeddings[1]),
    }


if __name__ == "__main__":
    text1 = sys.argv[1] if len(sys.argv) > 1 else "The cat sat on the mat"
    text2 = sys.argv[2] if len(sys.argv) > 2 else "A feline rested on the rug"

    result = get_similarity_with_usage(text1, text2)
    print(f"Similarity: {result['similarity_score']:.4f}")
    print(f"Model: {result['model']}")
    print(f"Token usage: {result['token_usage']}")
