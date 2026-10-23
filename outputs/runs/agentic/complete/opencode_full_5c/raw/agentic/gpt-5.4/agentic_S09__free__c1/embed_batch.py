from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient
from embeddings_models import normalize_texts


def embed_batch(texts: list[str]) -> dict[str, object]:
    normalized = normalize_texts(texts)
    client = CohereEmbeddingsClient()
    response = client.embed(normalized, input_type="classification")
    return {
        "provider": "cohere",
        "model": client.model,
        "count": len(normalized),
        "items": [
            {"text": text, "embedding": embedding, "dimensions": len(embedding)}
            for text, embedding in zip(normalized, response.embeddings)
        ],
    }
