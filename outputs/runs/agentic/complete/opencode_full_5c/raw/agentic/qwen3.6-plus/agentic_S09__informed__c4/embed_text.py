import os
from openai import OpenAI
from embeddings_client import get_openai_client, DEFAULT_EMBEDDING_MODEL


def embed_text(text: str, model: str = DEFAULT_EMBEDDING_MODEL) -> list[float]:
    client = get_openai_client()
    response = client.embeddings.create(
        input=text,
        model=model,
    )
    return response.data[0].embedding
