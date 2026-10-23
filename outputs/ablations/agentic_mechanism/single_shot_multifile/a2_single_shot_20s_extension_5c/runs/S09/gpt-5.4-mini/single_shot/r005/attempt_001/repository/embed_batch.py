import os
from embeddings_client import get_embedding_client
from embeddings_models import normalize_batch_text_input, normalize_embedding_response

DEFAULT_MODEL = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")


def embed_batch(texts: list[str], model: str = DEFAULT_MODEL) -> list[list[float]]:
    client = get_embedding_client()
    payload = normalize_batch_text_input(texts)
    response = client.embeddings.create(model=model, input=payload)
    return normalize_embedding_response(response)
