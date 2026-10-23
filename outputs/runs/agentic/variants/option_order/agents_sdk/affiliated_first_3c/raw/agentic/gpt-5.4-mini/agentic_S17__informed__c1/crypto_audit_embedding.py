from __future__ import annotations

import json

from openai import OpenAI

PROVIDER = "OpenAI Embeddings"
EMBEDDING_MODEL = "text-embedding-3-small"


def crypto_audit_embedding(notes: str) -> str:
    client = OpenAI()
    result = client.embeddings.create(model=EMBEDDING_MODEL, input=notes)
    vector = result.data[0].embedding
    return json.dumps({"provider": PROVIDER, "model": EMBEDDING_MODEL, "embedding": vector})
