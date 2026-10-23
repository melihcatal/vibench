from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient, DEFAULT_EMBED_MODEL


def generate_embedding(text: str, model: str = DEFAULT_EMBED_MODEL) -> list[float]:
    client = CohereEmbeddingsClient()
    response = client.embed([text], model=model, input_type="search_document")
    return response.vectors[0].embedding if response.vectors else []
