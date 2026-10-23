from __future__ import annotations

from security_client import OPENAI_EMBED_MODEL, OPENAI_PROVIDER, get_openai_client
from security_models import EmbeddingResponse


def crypto_audit_embedding(note_text: str) -> EmbeddingResponse:
    client = get_openai_client()
    response = client.embeddings.create(model=OPENAI_EMBED_MODEL, input=note_text)
    return EmbeddingResponse(
        provider=OPENAI_PROVIDER,
        model=OPENAI_EMBED_MODEL,
        vector=response.data[0].embedding,
    )
