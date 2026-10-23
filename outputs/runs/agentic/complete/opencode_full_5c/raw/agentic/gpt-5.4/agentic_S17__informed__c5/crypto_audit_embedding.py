from __future__ import annotations

from security_client import COHERE_EMBED_MODEL, COHERE_PROVIDER, get_cohere_client
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse


def crypto_audit_embedding(
    request: CryptoAuditEmbeddingRequest,
) -> CryptoAuditEmbeddingResponse:
    client = get_cohere_client()
    response = client.embed(
        model=COHERE_EMBED_MODEL,
        input_type=request.input_type,
        embedding_types=["float"],
        texts=request.notes,
    )
    return CryptoAuditEmbeddingResponse(
        provider=COHERE_PROVIDER,
        model=COHERE_EMBED_MODEL,
        embeddings=response.embeddings.float,
    )
