from __future__ import annotations

import os
from typing import Dict

from openai import OpenAI

from security_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def crypto_audit_embedding(note: str) -> Dict[str, object]:
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Missing OPENAI_API_KEY")
    client = OpenAI()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=note,
    )
    vector = response.data[0].embedding
    result = EmbeddingResult(
        provider="openai",
        model=OPENAI_EMBEDDING_MODEL,
        embedding=vector,
        dimensions=len(vector),
        usage=response.usage.model_dump()
        if hasattr(response.usage, "model_dump")
        else dict(response.usage),
    )
    return result.to_dict()
