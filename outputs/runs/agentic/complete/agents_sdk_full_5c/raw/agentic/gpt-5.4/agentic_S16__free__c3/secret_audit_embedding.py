from __future__ import annotations

import os
from typing import Optional

from openai import OpenAI

from security_models import EmbeddingResult


OPENAI_EMBED_MODEL = "text-embedding-3-small"


def embed_secret_audit_notes(notes: str, api_key: Optional[str] = None) -> EmbeddingResult:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBED_MODEL, input=notes)
    vector = list(response.data[0].embedding)
    return EmbeddingResult(
        provider="OpenAI",
        model=OPENAI_EMBED_MODEL,
        vector=vector,
        dimensions=len(vector),
    )
