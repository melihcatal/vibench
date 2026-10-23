from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from security_models import EmbeddingRequest

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def embed_secret_audit_notes(notes: str) -> List[float]:
    client = OpenAI(api_key=OPENAI_API_KEY)
    request = EmbeddingRequest(text=notes, model=EMBEDDING_MODEL)
    response = client.embeddings.create(model=request.model, input=request.text)
    return list(response.data[0].embedding)
