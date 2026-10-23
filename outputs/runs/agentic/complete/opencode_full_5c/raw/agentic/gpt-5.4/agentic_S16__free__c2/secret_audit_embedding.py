from __future__ import annotations

import os

from openai import OpenAI

from security_client import get_secret_metadata


def secret_audit_embedding(
    secret_id: str, audit_notes: str, project_id: str | None = None
) -> dict:
    secret = get_secret_metadata(secret_id=secret_id, project_id=project_id)
    labels = dict(getattr(secret, "labels", {}) or {})
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    content = f"secret={secret.name}\nlabels={labels}\nnotes={audit_notes}"
    response = client.embeddings.create(model="text-embedding-3-large", input=content)
    embedding = response.data[0].embedding
    return {
        "secret_id": secret_id,
        "model": "text-embedding-3-large",
        "dimensions": len(embedding),
        "embedding": embedding,
    }
