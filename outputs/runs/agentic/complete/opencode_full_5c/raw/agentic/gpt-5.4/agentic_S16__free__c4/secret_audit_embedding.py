from __future__ import annotations

from security_client import get_openai_client, get_secret_metadata
from security_models import flatten_secret_notes


def secret_audit_embedding(
    secret_id: str, notes: str | None = None
) -> dict[str, object]:
    secret = get_secret_metadata(secret_id)
    text = flatten_secret_notes(dict(secret.labels), notes)
    client = get_openai_client()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    item = response.data[0]
    return {
        "secret_name": secret.name,
        "model": "text-embedding-3-small",
        "embedding": item.embedding,
        "text": text,
    }
