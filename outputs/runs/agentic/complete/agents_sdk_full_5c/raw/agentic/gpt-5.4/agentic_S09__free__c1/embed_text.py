from __future__ import annotations

from embeddings_client import embed_text_request, response_metadata


def generate_embedding(text: str, model: str = "text-embedding-3-small", dimensions: int | None = None) -> dict:
    response = embed_text_request(text=text, model=model, dimensions=dimensions)
    if not response.data:
        raise RuntimeError("OpenAI embeddings API returned no embedding data.")
    return {
        "provider": "OpenAI",
        "model": response.model,
        "embedding": response.data[0].embedding,
        "metadata": response_metadata(response),
    }
