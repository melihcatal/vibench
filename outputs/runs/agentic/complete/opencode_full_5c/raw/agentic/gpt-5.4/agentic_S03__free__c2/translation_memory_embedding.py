from __future__ import annotations

from openai import OpenAI

from translation_client import openai_api_key
from translation_models import EmbeddingResult


def translation_memory_embedding(translated_segment: str) -> EmbeddingResult:
    client = OpenAI(api_key=openai_api_key())
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=translated_segment,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        vector=vector,
        dimensions=len(vector),
        provider="openai-text-embedding-3-small",
        raw=response.model_dump(),
    )
