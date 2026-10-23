from __future__ import annotations

from safety_client import DEFAULT_EMBEDDING_MODEL, get_openai_client


def moderation_reason_embedding(reason_text: str) -> dict:
    client = get_openai_client()
    response = client.embeddings.create(
        model=DEFAULT_EMBEDDING_MODEL,
        input=reason_text,
    )
    item = response.data[0]
    return {
        "provider": "OpenAI",
        "model": DEFAULT_EMBEDDING_MODEL,
        "embedding": item.embedding,
        "dimensions": len(item.embedding),
    }
