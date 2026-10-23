from __future__ import annotations

from typing import List

from openai import OpenAI

from security_models import EmbeddingResult

PROVIDER = "OpenAI"
MODEL = "text-embedding-3-small"


def embed_crypto_audit_notes(notes: str, api_key: str | None = None) -> EmbeddingResult:
    client = OpenAI(api_key=api_key)
    resp = client.embeddings.create(model=MODEL, input=notes)
    vector: List[float] = list(resp.data[0].embedding)
    return EmbeddingResult(text=notes, vector=vector, provider=PROVIDER)
