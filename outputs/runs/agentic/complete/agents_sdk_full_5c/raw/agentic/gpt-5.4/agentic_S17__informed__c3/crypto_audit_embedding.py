from __future__ import annotations

from security_client import get_openai_client
from security_models import EmbeddingResult, normalize_text_payload



def crypto_audit_embedding(text: str, model: str = "text-embedding-3-small") -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=model,
        input=normalize_text_payload(text),
    )
    item = response.data[0]
    return EmbeddingResult(
        provider="openai",
        model=model,
        dimensions=len(item.embedding),
        vector=item.embedding,
    )
