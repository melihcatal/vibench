from __future__ import annotations

import os

from openai import OpenAI

from security_client import default_project_id, get_secret_resource


def embed_secret_audit(secret_id: str, project_id: str | None = None) -> dict:
    secret = get_secret_resource(secret_id, project_id or default_project_id())
    audit_text = " ".join(
        [
            secret.name,
            " ".join(f"{k}:{v}" for k, v in dict(secret.labels).items()),
            " ".join(f"{k}:{v}" for k, v in dict(secret.annotations).items()),
        ]
    ).strip()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-large", input=audit_text
    )
    return {
        "secret_id": secret_id,
        "model": "text-embedding-3-large",
        "embedding": response.data[0].embedding,
    }
