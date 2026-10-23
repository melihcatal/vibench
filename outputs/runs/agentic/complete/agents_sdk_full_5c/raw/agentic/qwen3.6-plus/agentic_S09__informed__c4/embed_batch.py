"""
Generate embeddings for a batch of texts using OpenAI Embeddings API.

Uses the openai SDK with model text-embedding-3-small.
Requires OPENAI_API_KEY environment variable or explicit api_key parameter.
"""

from typing import List, Optional

from openai import OpenAI

from embeddings_client import get_openai_client, normalize_input_text
from embeddings_models import EmbeddingResponse, parse_batch_embedding_responses

OPENAI_MODEL = "text-embedding-3-small"
OPENAI_DEFAULT_DIMENSIONS = 1536
OPENAI_MAX_BATCH_SIZE = 2048


def embed_batch(
    texts: List[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
    dimensions: int = OPENAI_DEFAULT_DIMENSIONS,
    client: Optional[OpenAI] = None,
) -> List[EmbeddingResponse]:
    """
    Generate embeddings for a list of text strings via OpenAI.

    The OpenAI embeddings.create() endpoint accepts a list of strings as input,
    returning multiple embeddings in a single API call.

    Args:
        texts: List of input texts to embed.
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI embedding model identifier.
        dimensions: Output vector dimensions.
        client: Pre-configured OpenAI client (optional).

    Returns:
        List of EmbeddingResponse, one per input text in order.
    """
    if not texts:
        return []

    if len(texts) > OPENAI_MAX_BATCH_SIZE:
        raise ValueError(
            f"Batch size {len(texts)} exceeds OpenAI limit of {OPENAI_MAX_BATCH_SIZE}"
        )

    cleaned_texts = [normalize_input_text(t) for t in texts]

    if client is None:
        client = get_openai_client(api_key)

    payload = {"model": model, "input": cleaned_texts}
    if dimensions is not None:
        payload["dimensions"] = dimensions

    raw_response = client.embeddings.create(**payload)
    return parse_batch_embedding_responses(raw_response)


def embed_batch_in_chunks(
    texts: List[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
    dimensions: int = OPENAI_DEFAULT_DIMENSIONS,
    chunk_size: int = 500,
    client: Optional[OpenAI] = None,
) -> List[EmbeddingResponse]:
    """
    Embed a large list of texts by splitting into chunks.

    Useful when the number of texts exceeds the per-request limit.

    Args:
        texts: Full list of input texts.
        api_key: OpenAI API key.
        model: Embedding model ID.
        dimensions: Vector dimensions.
        chunk_size: Max texts per API call.
        client: Optional pre-built OpenAI client.

    Returns:
        Combined list of EmbeddingResponse for all texts in original order.
    """
    if not texts:
        return []

    if client is None:
        client = get_openai_client(api_key)

    all_responses = []
    for i in range(0, len(texts), chunk_size):
        chunk = texts[i : i + chunk_size]
        responses = embed_batch(
            texts=chunk,
            api_key=api_key,
            model=model,
            dimensions=dimensions,
            client=client,
        )
        all_responses.extend(responses)

    return all_responses
