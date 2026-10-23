"""
Embeds model outputs for clustering or retrieval using OpenAI Embeddings API.

Provider: OpenAI (api.openai.com)
Model family: text-embedding-3-small
"""

from typing import Optional, List

from model_client import get_sync_client, DEFAULT_EMBEDDING_MODEL
from model_models import (
    EmbeddingRequest,
    EmbeddingResponse,
)

OPENAI_API_HOST = "api.openai.com"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def generate_embedding(
    request: EmbeddingRequest,
    model: Optional[str] = None,
) -> EmbeddingResponse:
    """
    Generate an embedding vector for the provided text using OpenAI's
    text-embedding-3-small model hosted on api.openai.com.

    Args:
        request: EmbeddingRequest with text to embed.
        model: Optional explicit OpenAI embedding model identifier
               (e.g., text-embedding-3-small or text-embedding-3-large).

    Returns:
        EmbeddingResponse containing the embedding vector and metadata.
    """
    selected_model = model or DEFAULT_EMBEDDING_MODEL

    client = get_sync_client()

    response = client.embeddings.create(
        input=request.text,
        model=selected_model,
        encoding_format=request.encoding_format,
    )

    if response.data and len(response.data) > 0:
        embedding_data = response.data[0]
        vector = embedding_data.embedding
        dimensions = len(vector)
    else:
        vector = []
        dimensions = 0

    return EmbeddingResponse(
        vector=vector,
        dimensions=dimensions,
        model_used=selected_model,
    )


def generate_embeddings_batch(
    texts: List[str],
    model: Optional[str] = None,
    encoding_format: str = "float",
) -> List[EmbeddingResponse]:
    """
    Generate embeddings for multiple texts in a batch using OpenAI's
    text-embedding-3-small model.

    Args:
        texts: List of texts to embed.
        model: Optional explicit OpenAI embedding model identifier.
        encoding_format: Output format for embeddings.

    Returns:
        List of EmbeddingResponse objects.
    """
    selected_model = model or DEFAULT_EMBEDDING_MODEL

    client = get_sync_client()

    response = client.embeddings.create(
        input=texts,
        model=selected_model,
        encoding_format=encoding_format,
    )

    results = []
    for item in response.data:
        vector = item.embedding
        results.append(EmbeddingResponse(
            vector=vector,
            dimensions=len(vector),
            model_used=selected_model,
        ))

    return results


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vec_a: First embedding vector.
        vec_b: Second embedding vector.

    Returns:
        Cosine similarity score between 0.0 and 1.0.
    """
    import math

    if len(vec_a) != len(vec_b):
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


if __name__ == "__main__":
    sample = EmbeddingRequest(text="The quick brown fox jumps over the lazy dog.")
    result = generate_embedding(sample)
    print(f"Model: {result.model_used}")
    print(f"Dimensions: {result.dimensions}")
    print(f"Vector (first 5): {result.vector[:5]}")
