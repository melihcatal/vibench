from __future__ import annotations

from typing import Optional

from openai import OpenAI

from safety_models import EmbeddingRequest


EMBEDDING_MODEL = "text-embedding-3-small"


def moderation_reason_embedding(request: EmbeddingRequest, client: Optional[OpenAI] = None) -> list[float]:
    client = client or OpenAI()
    response = client.embeddings.create(model=request.model or EMBEDDING_MODEL, input=request.text)
    return response.data[0].embedding
