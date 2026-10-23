"""
Generate an embedding vector for a single text string using OpenAI Embeddings API.

Uses the openai SDK with model text-embedding-3-small.
Requires OPENAI_API_KEY environment variable or explicit api_key parameter.
"""

from typing import List, Optional

from openai import OpenAI

from embeddings_client import get_openai_client, normalize_input_text
from embeddings_models import EmbeddingRequest, EmbeddingResponse, parse_embedding_response

OPENAI_MODEL = "text-embedding-3-small"
OPENAI_DEFAULT_DIMENSIONS = 1536


def embed_text(
    text: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
    dimensions: int = OPENAI_DEFAULT_DIMENSIONS,
    client: Optional[OpenAI] = None,
) -> EmbeddingResponse:
    """
    Generate an embedding vector for one text string via OpenAI.

    Args:
        text: The input text to embed.
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI embedding model identifier.
        dimensions: Output vector dimensions.
        client: Pre-configured OpenAI client (optional).

    Returns:
        EmbeddingResponse containing the embedding vector, model ID, and usage.
    """
    cleaned_text = normalize_input_text(text)
    if client is None:
        client = get_openai_client(api_key)

    request = EmbeddingRequest(
        text=cleaned_text, model=model, dimensions=dimensions
    )

    raw_response = client.embeddings.create(**request.to_payload())
    return parse_embedding_response(raw_response)


def get_embedding_vector(
    text: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
    dimensions: int = OPENAI_DEFAULT_DIMENSIONS,
    client: Optional[OpenAI] = None,
) -> List[float]:
    """
    Convenience wrapper that returns just the raw embedding vector.

    Args:
        text: Input text.
        api_key: OpenAI API key.
        model: Embedding model ID.
        dimensions: Vector dimensions.
        client: Optional pre-built OpenAI client.

    Returns:
        List of floats representing the embedding.
    """
    response = embed_text(
        text=text, api_key=api_key, model=model, dimensions=dimensions, client=client
    )
    return response.embedding
