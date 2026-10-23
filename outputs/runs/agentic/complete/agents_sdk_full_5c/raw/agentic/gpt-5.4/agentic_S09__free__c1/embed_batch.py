from __future__ import annotations

from embeddings_client import embed_batch_request, response_metadata


def generate_batch_embeddings(texts: list[str], model: str = "text-embedding-3-small", dimensions: int | None = None) -> dict:
    response = embed_batch_request(texts=texts, model=model, dimensions=dimensions)
    embeddings = [item.embedding for item in sorted(response.data, key=lambda item: item.index)]
    return {
        "provider": "OpenAI",
        "model": response.model,
        "embeddings": embeddings,
        "metadata": response_metadata(response),
    }
