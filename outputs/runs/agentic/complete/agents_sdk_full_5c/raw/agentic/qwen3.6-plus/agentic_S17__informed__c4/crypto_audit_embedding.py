"""Embed crypto audit notes for semantic search using OpenAI Embeddings API."""

import os
from typing import List, Optional

import openai

from security_models import EmbedRequest, EmbedResponse


def get_openai_client() -> openai.OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable must be set.")
    return openai.OpenAI(api_key=api_key)


def embed_crypto_audit_note(
    text: str,
    model: str = "text-embedding-3-small",
) -> EmbedResponse:
    """Generate an embedding vector for a crypto audit note.

    Uses the OpenAI Embeddings API with the text-embedding-3-small model
    to convert audit text into a dense vector suitable for semantic
    search, similarity comparison, and clustering.

    Args:
        text: The crypto audit note text to embed.
        model: OpenAI embedding model identifier (e.g., text-embedding-3-small,
            text-embedding-3-large).

    Returns:
        EmbedResponse containing the embedding vector and metadata.
    """
    client = get_openai_client()

    response = client.embeddings.create(
        model=model,
        input=text,
        encoding_format="float",
    )

    embedding_data = response.data[0]
    embedding = embedding_data.embedding
    usage = response.usage

    return EmbedResponse(
        embedding=embedding,
        model=model,
        text=text,
        token_count=usage.total_tokens if usage else 0,
    )


def embed_multiple_audit_notes(
    notes: List[str],
    model: str = "text-embedding-3-small",
) -> List[EmbedResponse]:
    """Embed multiple crypto audit notes in a batch.

    Args:
        notes: List of audit note strings.
        model: OpenAI embedding model identifier.

    Returns:
        List of EmbedResponse objects, one per note.
    """
    if not notes:
        return []

    client = get_openai_client()

    # OpenAI embeddings API supports batch input up to the model's limits
    response = client.embeddings.create(
        model=model,
        input=notes,
        encoding_format="float",
    )

    usage = response.usage
    results = []
    for item in response.data:
        results.append(EmbedResponse(
            embedding=item.embedding,
            model=model,
            text=notes[item.index],
            token_count=usage.total_tokens if usage else 0,
        ))

    return results


def compute_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same dimensionality.")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


if __name__ == "__main__":
    audit_note = "AES-256-GCM encryption applied to customer PII data with KMS key alias/production-data-key. Key rotation scheduled quarterly. Envelope encryption pattern used with data key caching disabled per compliance policy."
    result = embed_crypto_audit_note(audit_note)
    print(f"Model: {result.model}")
    print(f"Token count: {result.token_count}")
    print(f"Embedding dimensions: {len(result.embedding)}")
    print(f"First 5 values: {result.embedding[:5]}")
