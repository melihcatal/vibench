from __future__ import annotations

from security_client import config, openai_client
from security_models import EmbeddingResult



def embed_crypto_audit_notes(text: str) -> EmbeddingResult:
    client = openai_client()
    response = client.embeddings.create(
        model=config.openai_embed_model,
        input=text,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        provider="openai",
        model=config.openai_embed_model,
        vector=vector,
        dimensions=len(vector),
    )
