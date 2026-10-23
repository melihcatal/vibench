"""Generates embeddings for a batch of texts using OpenAI Embeddings API.

Uses the text-embedding-3-small model from OpenAI to produce embeddings for
multiple texts in a single API call.
"""

import os
from typing import List

from embeddings_client import get_openai_client, create_batch_embeddings, get_embedding_model
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_texts_batch(
    texts: List[str],
    model: str = None,
    dimensions: int = None,
) -> List[List[float]]:
    """Generate embeddings for a batch of texts.

    Args:
        texts: List of input text strings to embed.
        model: OpenAI embedding model ID (defaults to OPENAI_EMBEDDING_MODEL env var
               or text-embedding-3-small).
        dimensions: Optional output dimensionality.

    Returns:
        List of embedding vectors, one per input text.
    """
    client = get_openai_client()
    model_id = model or get_embedding_model()

    request = EmbeddingRequest(
        texts=texts,
        model=model_id,
        dimensions=dimensions,
    )

    embeddings = create_batch_embeddings(
        client=client,
        texts=texts,
        model=model_id,
        dimensions=dimensions,
    )

    return embeddings


def embed_texts_batch_with_metadata(
    texts: List[str],
    model: str = None,
    dimensions: int = None,
) -> EmbeddingResponse:
    """Generate embeddings for a batch and return structured response.

    Args:
        texts: List of input text strings to embed.
        model: OpenAI embedding model ID.
        dimensions: Optional output dimensionality.

    Returns:
        EmbeddingResponse containing embeddings and metadata.
    """
    client = get_openai_client()
    model_id = model or get_embedding_model()

    request_params = EmbeddingRequest(
        texts=texts,
        model=model_id,
        dimensions=dimensions,
    ).to_api_params()

    response = client.embeddings.create(**request_params)

    embeddings = [item.embedding for item in response.data]
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return EmbeddingResponse(
        embeddings=embeddings,
        model=model_id,
        usage=usage,
        original_texts=texts,
    )


def main():
    texts = [
        "Machine learning is a subset of artificial intelligence.",
        "Natural language processing enables computers to understand text.",
        "Computer vision allows machines to interpret visual data.",
    ]
    model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

    response = embed_texts_batch_with_metadata(texts, model=model)
    print(f"Model: {response.model}")
    print(f"Texts processed: {len(texts)}")
    print(f"Usage: {response.usage}")
    for text, emb in response.text_embedding_pairs():
        print(f"  '{text[:50]}...' -> dim={len(emb)}")


if __name__ == "__main__":
    main()
