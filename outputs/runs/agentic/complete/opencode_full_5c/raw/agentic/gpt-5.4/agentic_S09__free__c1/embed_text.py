from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient
from embeddings_models import normalize_text


def embed_text(text: str) -> dict[str, object]:
    client = CohereEmbeddingsClient()
    cleaned = normalize_text(text)
    response = client.embed([cleaned], input_type="search_document")
    return {
        "provider": "cohere",
        "model": client.model,
        "text": cleaned,
        "embedding": response.embeddings[0],
        "dimensions": len(response.embeddings[0]),
    }
