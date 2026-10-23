from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from security_models import EmbeddingResult


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"



def crypto_audit_embedding(note: str, model: str = DEFAULT_EMBEDDING_MODEL) -> EmbeddingResult:
    client = OpenAI()
    response = client.embeddings.create(
        model=model,
        input=note,
    )
    item = response.data[0]
    vector = list(item.embedding)
    return EmbeddingResult(
        provider="openai",
        model=model,
        vector=vector,
        dimensions=len(vector),
    )



def crypto_audit_embedding_dict(note: str, model: str = DEFAULT_EMBEDDING_MODEL) -> Dict[str, Any]:
    result = crypto_audit_embedding(note=note, model=model)
    return {
        "provider": result.provider,
        "model": result.model,
        "vector": result.vector,
        "dimensions": result.dimensions,
    }
