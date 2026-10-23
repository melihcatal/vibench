from __future__ import annotations

import os

from openai import OpenAI

from security_models import EmbeddingResult

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def secret_audit_embedding(notes: str) -> EmbeddingResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=notes)
    vector = list(response.data[0].embedding)
    return EmbeddingResult(text=notes, vector=vector, model=OPENAI_EMBEDDING_MODEL)
