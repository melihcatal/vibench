from __future__ import annotations

from safety_client import SafetyClient
from safety_models import EmbeddingRequest

EMBEDDING_MODEL = "openai:text-embedding-3-small"


def moderation_reason_embedding(rationales: list[str]) -> dict:
    client = SafetyClient()
    result = client.embed_rationale(EmbeddingRequest(texts=rationales))
    return {"provider": "OpenAI", "model": EMBEDDING_MODEL, "embeddings": result["embeddings"]}
