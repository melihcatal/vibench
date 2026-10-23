from __future__ import annotations

from typing import Any, Dict

from security_client import get_openai_client
from security_models import EmbeddingResult


def crypto_audit_embedding(note_text: str) -> Dict[str, Any]:
    client = get_openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=note_text,
    )
    vector = response.data[0].embedding
    result = EmbeddingResult(
        provider="openai",
        model="text-embedding-3-large",
        vector=vector,
        dimensions=len(vector),
    )
    return result.to_dict()
