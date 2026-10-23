"""
Generate an embedding vector for one text string.

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


def embed_text(
    text: str,
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> List[float]:
    """
    Generate an embedding vector for a single text string using OpenAI's API.

    Args:
        text: The text string to embed
        model: OpenAI embedding model (default: text-embedding-3-small)
        dimensions: Optional embedding dimensionality
        api_key: OpenAI API key (falls back to OPENAI_API_KEY env var)

    Returns:
        Embedding vector as a list of floats

    Raises:
        ValueError: If text is empty or API key is missing
        openai.APIError: If the OpenAI API request fails
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    config = load_embeddings_config()
    target_model = model or config["model"]
    target_dimensions = dimensions or config["dimensions"]

    request = EmbeddingRequest(
        texts=[text],
        model=target_model,
        dimensions=target_dimensions,
    )
    request.validate()

    client = get_openai_client(api_key=api_key)
    payload = build_embeddings_payload(
        texts=[text],
        model=target_model,
        dimensions=target_dimensions,
    )

    response = client.embeddings.create(**payload)
    embeddings = parse_embeddings_response(response)

    result = EmbeddingResponse(
        embeddings=embeddings,
        model=response.model,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    )

    return result.embeddings[0]


if __name__ == "__main__":
    import os
    import json

    sample_text = "OpenAI embeddings provide semantic understanding of text."
    embedding = embed_text(sample_text)
    print(json.dumps({
        "text": sample_text,
        "model": "text-embedding-3-small",
        "dimensions": len(embedding),
        "embedding_preview": embedding[:5],
    }, indent=2))
