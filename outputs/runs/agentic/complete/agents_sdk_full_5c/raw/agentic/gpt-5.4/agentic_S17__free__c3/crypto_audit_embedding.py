from __future__ import annotations

from security_client import get_openai_client
from security_models import EmbeddingResult


OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def crypto_audit_embedding(note_text: str) -> EmbeddingResult:
    client = get_openai_client()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=note_text,
    )
    vector = response.data[0].embedding
    return EmbeddingResult(
        vector=vector,
        provider="OpenAI",
        model=OPENAI_EMBEDDING_MODEL,
    )
