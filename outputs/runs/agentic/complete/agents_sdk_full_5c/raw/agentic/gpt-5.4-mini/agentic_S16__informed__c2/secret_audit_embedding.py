from __future__ import annotations

from openai import OpenAI

from security_models import EmbeddingRequest

MODEL_ID = "text-embedding-3-small"


def embed_audit_note(note: str) -> list[float]:
    client = OpenAI()
    request = EmbeddingRequest(text=note, model=MODEL_ID)
    result = client.embeddings.create(model=request.model, input=request.text)
    return result.data[0].embedding
