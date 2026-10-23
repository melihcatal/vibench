import os
from typing import List
from security_client import SecurityClient
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse


def embed_crypto_audit_notes(
    request: CryptoAuditEmbeddingRequest,
) -> CryptoAuditEmbeddingResponse:
    client = SecurityClient()
    embedding = client.embed_text_with_vertex_ai(
        project_id=request.project_id,
        location_id=request.location_id,
        document_content=request.document_content,
    )
    return CryptoAuditEmbeddingResponse(embedding=embedding)
