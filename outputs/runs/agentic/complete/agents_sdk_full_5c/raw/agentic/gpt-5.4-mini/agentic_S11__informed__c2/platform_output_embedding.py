from __future__ import annotations

from openai import AzureOpenAI

from model_client import get_client
from model_models import normalize_text


def platform_output_embedding(text: str) -> list[float]:
    client: AzureOpenAI = get_client()
    embedding = client.embeddings.create(
        model="text-embedding-3-large",
        input=normalize_text(text),
    )
    return list(embedding.data[0].embedding)
