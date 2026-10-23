from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from security_models import AuditEmbeddingResult


_PROVIDER = "openai"
_MODEL = "text-embedding-3-small"


def secret_audit_embedding(notes: str) -> AuditEmbeddingResult:
    client = OpenAI()
    response = client.embeddings.create(model=_MODEL, input=notes)
    vector: List[float] = list(response.data[0].embedding)
    return AuditEmbeddingResult(provider=_PROVIDER, text=notes, vector=vector)


if __name__ == "__main__":
    notes = os.environ.get("AUDIT_NOTES", "Secret rotation completed without incident.")
    embedding = secret_audit_embedding(notes)
    print(len(embedding.vector))
