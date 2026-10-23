"""
Generates an embedding vector for one text string using OpenAI API.
Provider: OpenAI (api.openai.com)
Model: text-embedding-3-small
"""

import sys
from typing import List, Optional

from embeddings_client import get_openai_client, resolve_model, extract_embedding_vector, get_token_usage
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_single_text(
    text: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> EmbeddingResponse:
    """
    Generate an embedding vector for a single text string using OpenAI embeddings API.

    Args:
        text: The text to embed.
        model: OpenAI embedding model (default: text-embedding-3-small).
        dimensions: Output dimensionality for the embedding.
        api_key: OpenAI API key.

    Returns:
        EmbeddingResponse containing the vector and metadata.
    """
    resolved_model = resolve_model(model)

    client = get_openai_client(api_key=api_key)

    request = EmbeddingRequest(
        text=text,
        model=resolved_model,
        dimensions=dimensions,
    )

    response = client.embeddings.create(**request.to_openai_payload())

    return EmbeddingResponse.from_openai_response(response)


def embed_text_to_list(
    text: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> List[float]:
    """
    Generate and return just the embedding vector as a list of floats.

    Args:
        text: The text to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions.
        api_key: OpenAI API key.

    Returns:
        List of floats representing the embedding vector.
    """
    response = embed_single_text(text, model=model, dimensions=dimensions, api_key=api_key)
    return response.embedding


if __name__ == "__main__":
    input_text = sys.argv[1] if len(sys.argv) > 1 else "Hello, world!"
    result = embed_single_text(input_text)
    print(f"Model: {result.model}")
    print(f"Dimensions: {len(result.embedding)}")
    print(f"Usage: {result.usage_tokens} tokens")
    print(f"Vector (first 5): {result.embedding[:5]}")
