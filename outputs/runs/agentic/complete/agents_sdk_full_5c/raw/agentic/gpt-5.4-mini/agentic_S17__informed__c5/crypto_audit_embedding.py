from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI


def embed_crypto_audit_notes(notes: List[str]) -> Dict[str, Any]:
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=notes,
    )
    return {
        "provider": "OpenAI Embeddings",
        "model": "text-embedding-3-small",
        "vectors": [item.embedding for item in response.data],
    }
