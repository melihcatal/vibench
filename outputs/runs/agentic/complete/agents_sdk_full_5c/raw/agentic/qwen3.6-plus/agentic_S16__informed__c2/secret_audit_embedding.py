"""Embed secret audit notes for semantic search using OpenAI Embeddings API.

Provider: OpenAI Embeddings API (openai SDK)
Auth: OPENAI_API_KEY
Model: text-embedding-3-small
"""

import os
from openai import OpenAI

from security_models import SecretFetchResponse


def embed_audit_notes(
    audit_notes: str,
    model: str = "text-embedding-3-small",
) -> dict:
    """Generate embeddings for secret audit notes using OpenAI's text-embedding-3-small model.

    Returns the embedding vector and metadata.
    """
    if not audit_notes or not audit_notes.strip():
        return {
            "status": "no_content",
            "embedding": None,
            "model": model,
            "provider": "openai",
        }

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error": "OPENAI_API_KEY environment variable not set",
            "provider": "openai",
        }

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            input=audit_notes,
            model=model,
        )

        embedding_data = response.data[0]
        return {
            "status": "success",
            "embedding": embedding_data.embedding,
            "model": model,
            "provider": "openai",
            "embedding_length": len(embedding_data.embedding),
            "input_tokens": response.usage.prompt_tokens,
        }

    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "provider": "openai",
            "model": model,
        }


def embed_secret_audit_response(
    response: SecretFetchResponse,
    model: str = "text-embedding-3-small",
) -> dict:
    """Embed audit-related metadata from a SecretFetchResponse."""
    metadata = response.metadata or {}
    audit_notes = metadata.get(
        "audit_notes",
        f"Secret {response.secret_name} version {response.version_id or 'latest'} "
        f"retrieved from {response.provider}.",
    )
    return embed_audit_notes(audit_notes=audit_notes, model=model)


def build_search_index(entries: list[dict]) -> dict:
    """Build a simple in-memory search index from multiple embedded audit notes.

    Returns a dict mapping index positions to their source text and embedding.
    """
    index = {}
    for i, entry in enumerate(entries):
        result = embed_audit_notes(entry.get("text", ""))
        if result.get("embedding"):
            index[i] = {
                "text": entry["text"],
                "embedding": result["embedding"],
                "source": entry.get("source", ""),
            }
    return {"index": index, "size": len(index), "provider": "openai"}


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    import math

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    result = embed_audit_notes(
        audit_notes="Production API key rotated on schedule. Previous version deprecated.",
    )
    print(f"Status: {result.get('status')}")
    print(f"Embedding length: {result.get('embedding_length')}")
    print(f"Model: {result.get('model')}")
