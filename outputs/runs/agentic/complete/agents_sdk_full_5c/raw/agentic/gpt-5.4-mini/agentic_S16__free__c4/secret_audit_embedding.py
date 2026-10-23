from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from security_models import SecretAnalysisRequest, SecretAnalysisResponse


client = OpenAI()


def embed_secret_audit_notes(notes: str) -> SecretAnalysisResponse:
    request = SecretAnalysisRequest(label="audit-notes", notes=notes, provider="openai")
    embedding = client.embeddings.create(model="text-embedding-3-small", input=request.notes)
    vector: List[float] = list(embedding.data[0].embedding)
    return SecretAnalysisResponse(risk_level="info", summary="Embedded audit notes for semantic search.", provider=request.provider, metadata={"dimensions": len(vector), "vector": vector})


if __name__ == "__main__":
    print(embed_secret_audit_notes(os.environ.get("AUDIT_NOTES", "secret rotation audit" )).summary)
