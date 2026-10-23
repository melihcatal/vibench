from __future__ import annotations

from speech_client import OPENAI_EMBEDDING_MODEL, get_openai_client


def embed_script(text: str) -> dict:
    client = get_openai_client()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    item = response.data[0]
    return {
        "provider": "openai",
        "model": OPENAI_EMBEDDING_MODEL,
        "embedding": item.embedding,
        "dimensions": len(item.embedding),
    }
