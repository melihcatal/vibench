import os

from embeddings_client import get_openai_client
from embeddings_models import normalize_embedding

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_text(text: str, model: str = OPENAI_EMBEDDING_MODEL) -> list[float]:
    client = get_openai_client()
    response = client.embeddings.create(model=model, input=text)
    return normalize_embedding(response.data[0].embedding)
