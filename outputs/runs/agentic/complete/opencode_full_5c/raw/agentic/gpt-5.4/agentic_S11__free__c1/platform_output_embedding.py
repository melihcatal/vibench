from __future__ import annotations

from model_client import get_embedding_model, get_openai_client


def platform_output_embedding(text: str) -> object:
    client = get_openai_client()
    return client.embeddings.create(
        model=get_embedding_model(),
        input=text,
    )
