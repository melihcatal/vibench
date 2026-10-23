"""
Generate embeddings for a batch of texts.

Provider: OpenAI Embeddings API (https://api.openai.com)
Model: text-embedding-3-small
"""

from typing import List, Optional

from embeddings_client import (
    get_openai_client,
    load_embeddings_config,
    build_embeddings_payload,
    parse_embeddings_response,
)
from embeddings_models import EmbeddingRequest, EmbeddingResponse


BATCH_SIZE_LIMIT = 2048  # OpenAI API batch input limit


def embed_batch(
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    batch_size: int = 100,
) -> List[List[float]]:
    """
    Generate embeddings for a batch of text strings using OpenAI's API.

    Processes texts in chunks to respect OpenAI API rate limits and input size
    constraints.

    Args:
        texts: List of text strings to embed
        model: OpenAI embedding model (default: text-embedding-3-small)
        dimensions: Optional embedding dimensionality
        api_key: OpenAI API key (falls back to OPENAI_API_KEY env var)
        batch_size: Number of texts per API call (max 2048 for OpenAI)

    Returns:
        List of embedding vectors, one per input text

    Raises:
        ValueError: If texts list is empty or contains empty strings
        openai.APIError: If the OpenAI API request fails
    """
    if not texts:
        raise ValueError("texts list cannot be empty")

    request = EmbeddingRequest(
        texts=texts,
        model=model or "text-embedding-3-small",
        dimensions=dimensions,
    )
    request.validate()

    config = load_embeddings_config()
    target_model = model or config["model"]
    target_dimensions = dimensions or config["dimensions"]

    client = get_openai_client(api_key=api_key)
    all_embeddings: List[List[float]] = []

    effective_batch_size = min(batch_size, BATCH_SIZE_LIMIT)

    for i in range(0, len(texts), effective_batch_size):
        batch = texts[i:i + effective_batch_size]
        payload = build_embeddings_payload(
            texts=batch,
            model=target_model,
            dimensions=target_dimensions,
        )

        response = client.embeddings.create(**payload)
        batch_embeddings = parse_embeddings_response(response)
        all_embeddings.extend(batch_embeddings)

    result = EmbeddingResponse(
        embeddings=all_embeddings,
        model=target_model,
        usage={"batch_count": (len(texts) + effective_batch_size - 1) // effective_batch_size},
    )

    return result.embeddings


if __name__ == "__main__":
    import json

    sample_texts = [
        "Machine learning enables computers to learn from data.",
        "Neural networks are inspired by biological neurons.",
        "Natural language processing bridges human language and computers.",
    ]
    embeddings = embed_batch(sample_texts)
    print(json.dumps({
        "texts_count": len(sample_texts),
        "model": "text-embedding-3-small",
        "dimensions": len(embeddings[0]),
        "embeddings_count": len(embeddings),
    }, indent=2))
