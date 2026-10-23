from __future__ import annotations

from security_client import get_openai_client
from security_models import EmbeddingResponse


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_crypto_audit_notes(text: str) -> EmbeddingResponse:
    client = get_openai_client()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=text,
    )
    vector = response.data[0].embedding
    return EmbeddingResponse(
        text=text,
        embedding=vector,
        dimensions=len(vector),
        provider="openai",
        model=OPENAI_EMBEDDING_MODEL,
    )
