from __future__ import annotations

from openai import OpenAI

from safety_client import safety_model_name
from safety_models import EmbeddingResult


def moderation_reason_embedding(reason: str) -> EmbeddingResult:
    client = OpenAI()
    response = client.embeddings.create(  # openai SDK
        model=safety_model_name("embedding"),
        input=reason,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(embedding=vector, model=safety_model_name("embedding"))
