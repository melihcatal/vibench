"""
Generates embeddings for a batch of texts using OpenAI API.
Provider: OpenAI (api.openai.com)
Model: text-embedding-3-small
"""

import sys
from typing import List, Optional, Dict, Any

from embeddings_client import (
    get_openai_client,
    resolve_model,
    build_batch_embedding_payload,
    extract_batch_embeddings,
    get_token_usage,
)
from embeddings_models import BatchEmbeddingRequest, BatchEmbeddingResponse


def embed_batch_texts(
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> BatchEmbeddingResponse:
    """
    Generate embeddings for a batch of text strings using OpenAI embeddings API.

    Args:
        texts: List of text strings to embed.
        model: OpenAI embedding model (default: text-embedding-3-small).
        dimensions: Output dimensionality for each embedding.
        api_key: OpenAI API key.

    Returns:
        BatchEmbeddingResponse containing all vectors and metadata.
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

    return BatchEmbeddingResponse.from_openai_response(response)


def embed_batch_to_dict(
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> Dict[str, List[float]]:
    """
    Generate embeddings and return as a dict mapping text to vector.

    Args:
        texts: List of text strings to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions.
        api_key: OpenAI API key.

    Returns:
        Dictionary mapping each input text to its embedding vector.
    """
    response = embed_batch_texts(texts, model=model, dimensions=dimensions, api_key=api_key)
    return {text: vec for text, vec in zip(texts, response.embeddings)}


def embed_batch_with_indices(
    texts: List[str],
    model: Optional[str] = None,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Generate embeddings and return as list of dicts with index, text, and vector.

    Args:
        texts: List of text strings to embed.
        model: OpenAI embedding model identifier.
        dimensions: Optional output dimensions.
        api_key: OpenAI API key.

    Returns:
        List of dicts with 'index', 'text', and 'embedding' keys.
    """
    response = embed_batch_texts(texts, model=model, dimensions=dimensions, api_key=api_key)
    return [
        {
            "index": i,
            "text": text,
            "embedding": vec,
        }
        for i, (text, vec) in enumerate(zip(texts, response.embeddings))
    ]


if __name__ == "__main__":
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a popular programming language.",
        "Machine learning models require quality data.",
    ]

    results = embed_batch_texts(sample_texts)
    print(f"Model: {results.models[0]}")
    print(f"Batch size: {len(results.embeddings)}")
    print(f"Total usage: {results.total_usage_tokens} tokens")
    print(f"First vector dims: {len(results.embeddings[0])}")
