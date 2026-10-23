from __future__ import annotations

from typing import List

from openai import OpenAI

from safety_models import EmbeddingRequest

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_moderation_reasons(reasons: List[str]) -> List[List[float]]:
    client = OpenAI()
    req = EmbeddingRequest(texts=reasons)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=req.texts)
    return [item.embedding for item in response.data]
