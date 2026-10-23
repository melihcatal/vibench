from __future__ import annotations

from embeddings_client import get_client, load_settings
from embeddings_models import normalize_texts, normalize_vector


def embed_text(text: str) -> list[float]:
    settings = load_settings()
    client = get_client(settings)
    cleaned = normalize_texts([text])[0]
    response = client.embeddings.create(model=settings.embedding_model, input=cleaned)
    return normalize_vector(response.data[0].embedding)
