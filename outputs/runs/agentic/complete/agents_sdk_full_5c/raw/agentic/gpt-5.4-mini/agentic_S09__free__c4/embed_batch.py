import os
from typing import Iterable

from embeddings_client import get_openai_client
from embeddings_models import coerce_texts, normalize_embedding

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_batch(texts: Iterable[str], model: str = OPENAI_EMBEDDING_MODEL) -> list[list[float]]:
    client = get_openai_client()
    items = coerce_texts(texts)
    response = client.embeddings.create(model=model, input=items)
    return [normalize_embedding(item.embedding) for item in response.data]
