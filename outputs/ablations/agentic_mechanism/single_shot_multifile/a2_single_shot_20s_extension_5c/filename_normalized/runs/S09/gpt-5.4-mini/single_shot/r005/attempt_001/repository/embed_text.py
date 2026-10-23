import os
from embeddings_client import get_embedding_client
from embeddings_models import normalize_embedding_response, normalize_single_text_input

DEFAULT_MODEL = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")


def embed_text(text: str, model: str = DEFAULT_MODEL) -> list[float]:
    client = get_embedding_client()
    payload = normalize_single_text_input(text)
    response = client.embeddings.create(model=model, input=payload)
    normalized = normalize_embedding_response(response)
    return normalized[0]
