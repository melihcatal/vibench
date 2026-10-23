import os
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_single_embedding


def embed_text(text: str, model: str | None = None) -> list[float]:
    client = get_embeddings_client()
    model_name = model or os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    response = client.embeddings.create(model=model_name, input=text)
    return normalize_single_embedding(response)
