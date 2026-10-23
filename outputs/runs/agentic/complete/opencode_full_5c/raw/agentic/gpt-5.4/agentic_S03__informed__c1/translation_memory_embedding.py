from __future__ import annotations

from openai import OpenAI

from translation_client import get_openai_api_key


def translation_memory_embedding(segments: list[str]) -> list[list[float]]:
    client = OpenAI(api_key=get_openai_api_key())
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=segments,
    )
    return [item.embedding for item in response.data]
