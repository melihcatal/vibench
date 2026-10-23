from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from security_models import EmbeddingDocument

# OpenAI embeddings integration
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def secret_audit_embedding(document_id: str, text: str, metadata: dict | None = None) -> EmbeddingDocument:
    client = OpenAI()
    result = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    embedding: List[float] = list(result.data[0].embedding)
    return EmbeddingDocument(document_id=document_id, text=text, embedding=embedding, metadata=metadata or {})
