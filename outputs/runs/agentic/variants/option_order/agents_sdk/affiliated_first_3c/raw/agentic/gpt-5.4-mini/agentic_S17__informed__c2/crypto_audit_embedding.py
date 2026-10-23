from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_crypto_audit_notes(notes: List[str], api_key: str | None = None) -> Dict[str, Any]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=notes)
    return {
        "service": "OpenAI Embeddings",
        "model": OPENAI_EMBEDDING_MODEL,
        "vectors": [item.embedding for item in response.data],
    }
