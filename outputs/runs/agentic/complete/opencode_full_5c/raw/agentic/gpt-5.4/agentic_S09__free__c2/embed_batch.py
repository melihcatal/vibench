from __future__ import annotations

from embeddings_client import CohereEmbeddingsClient, DEFAULT_EMBED_MODEL


def generate_batch_embeddings(
    texts: list[str], model: str = DEFAULT_EMBED_MODEL
) -> list[list[float]]:
    client = CohereEmbeddingsClient()
    response = client.embed(texts, model=model, input_type="search_document")
    return [item.embedding for item in response.vectors]
