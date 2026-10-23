from __future__ import annotations

from openai import OpenAI

from safety_models import EmbeddingResult


client = OpenAI()


def moderation_reason_embedding(text: str) -> EmbeddingResult:
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    vector = response.data[0].embedding
    return EmbeddingResult(vector=vector, provider="OpenAI", model="text-embedding-3-small")
