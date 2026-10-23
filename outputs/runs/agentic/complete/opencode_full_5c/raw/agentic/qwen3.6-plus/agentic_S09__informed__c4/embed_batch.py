import os
from openai import OpenAI
from embeddings_client import get_openai_client, DEFAULT_EMBEDDING_MODEL


def embed_batch(
    texts: list[str], model: str = DEFAULT_EMBEDDING_MODEL
) -> list[list[float]]:
    client = get_openai_client()
    response = client.embeddings.create(
        input=texts,
        model=model,
    )
    sorted_data = sorted(response.data, key=lambda d: d.index)
    return [item.embedding for item in sorted_data]
