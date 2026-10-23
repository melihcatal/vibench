from __future__ import annotations

import os

from openai import OpenAI


def embed_caption_chunks(chunks: list[str]) -> dict[str, object]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI embeddings")
    client = OpenAI(api_key=api_key)
    cleaned_chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    response = client.embeddings.create(
        model="text-embedding-3-small", input=cleaned_chunks
    )
    embeddings = [item.embedding for item in response.data]
    return {
        "model": "text-embedding-3-small",
        "embeddings": embeddings,
        "count": len(embeddings),
    }
