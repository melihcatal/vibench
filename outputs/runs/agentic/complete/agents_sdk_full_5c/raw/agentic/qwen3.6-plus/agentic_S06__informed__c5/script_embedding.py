"""Embed narration scripts for voice-asset search using OpenAI Embeddings API."""

import os
from typing import Optional

from openai import OpenAI


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_key() -> str:
    """Retrieve the OpenAI API key from environment."""
    key = os.environ.get(OPENAI_API_KEY_ENV)
    if not key:
        raise ValueError(f"{OPENAI_API_KEY_ENV} environment variable is required")
    return key


def create_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Create an authenticated OpenAI client instance."""
    key = api_key or get_openai_key()
    return OpenAI(api_key=key)


def embed_script(
    text: str,
    *,
    model: str = DEFAULT_EMBEDDING_MODEL,
    client: Optional[OpenAI] = None,
) -> list[float]:
    """Generate an embedding vector for a narration script using OpenAI.

    Uses the OpenAI embeddings API (model: text-embedding-3-small) to
    produce a dense vector representation of the narration text for
    downstream voice-asset similarity search.

    Args:
        text: The narration script text to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        client: Optional pre-configured OpenAI client instance.

    Returns:
        A list of floats representing the embedding vector.
    """
    if client is None:
        client = create_openai_client()

    response = client.embeddings.create(
        input=text,
        model=model,
    )

    return response.data[0].embedding


def embed_scripts_batch(
    texts: list[str],
    *,
    model: str = DEFAULT_EMBEDDING_MODEL,
    client: Optional[OpenAI] = None,
) -> list[list[float]]:
    """Generate embeddings for a batch of narration scripts using OpenAI.

    Args:
        texts: List of narration script texts to embed.
        model: OpenAI embedding model identifier (default: text-embedding-3-small).
        client: Optional pre-configured OpenAI client instance.

    Returns:
        List of embedding vectors, one per input text.
    """
    if client is None:
        client = create_openai_client()

    response = client.embeddings.create(
        input=texts,
        model=model,
    )

    sorted_data = sorted(response.data, key=lambda d: d.index)
    return [d.embedding for d in sorted_data]


def compute_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = sum(a * a for a in vector_a) ** 0.5
    magnitude_b = sum(b * b for b in vector_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def search_voice_assets(
    query_text: str,
    asset_texts: list[str],
    asset_ids: Optional[list[str]] = None,
    *,
    model: str = DEFAULT_EMBEDDING_MODEL,
    client: Optional[OpenAI] = None,
    top_k: int = 5,
) -> list[dict]:
    """Search for matching voice assets by embedding similarity using OpenAI.

    Embeds the query text and candidate asset texts using OpenAI's
    text-embedding-3-small model, then ranks assets by cosine similarity.

    Args:
        query_text: The query narration text.
        asset_texts: List of voice asset descriptions to search over.
        asset_ids: Optional list of asset identifiers.
        model: OpenAI embedding model identifier.
        client: Optional pre-configured OpenAI client.
        top_k: Maximum number of results to return.

    Returns:
        Ranked list of matching assets with similarity scores.
    """
    if asset_ids is None:
        asset_ids = [str(i) for i in range(len(asset_texts))]

    query_embedding = embed_script(query_text, model=model, client=client)
    asset_embeddings = embed_scripts_batch(asset_texts, model=model, client=client)

    scored = []
    for i, asset_emb in enumerate(asset_embeddings):
        similarity = compute_similarity(query_embedding, asset_emb)
        scored.append({
            "asset_id": asset_ids[i],
            "text": asset_texts[i],
            "similarity": similarity,
        })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]
