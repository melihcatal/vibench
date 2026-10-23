import os
from security_client import get_openai_client
from security_models import EmbeddingRequest, EmbeddingResponse


def embed_crypto_audit_notes(audit_notes: str) -> EmbeddingResponse:
    """Embed crypto audit notes for semantic search using OpenAI embeddings."""
    client = get_openai_client()

    try:
        response = client.embeddings.create(
            model="text-embedding-3-small", input=audit_notes, encoding_format="float"
        )

        embedding = response.data[0].embedding

        return EmbeddingResponse(
            success=True,
            embedding=embedding,
            model="text-embedding-3-small",
            provider="openai",
        )
    except Exception as e:
        return EmbeddingResponse(success=False, error=str(e), provider="openai")
