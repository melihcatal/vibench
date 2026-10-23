from __future__ import annotations

from model_client import DEFAULT_EMBEDDING_MODEL, get_openai_client


def embed_output(text: str) -> list[float]:
    client = get_openai_client()
    response = client.embeddings.create(
        model=DEFAULT_EMBEDDING_MODEL,
        input=text,
    )
    return list(response.data[0].embedding)
