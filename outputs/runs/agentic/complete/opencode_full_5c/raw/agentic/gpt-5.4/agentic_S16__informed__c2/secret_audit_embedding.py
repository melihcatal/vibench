from __future__ import annotations

from security_client import get_openai_client


def secret_audit_embedding(text: str) -> list[float]:
    client = get_openai_client()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
