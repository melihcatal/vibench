import os
import cohere
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse


def get_audit_embedding(
    request: CryptoAuditEmbeddingRequest,
) -> CryptoAuditEmbeddingResponse:
    """
    Embed crypto audit notes for semantic search using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=request.notes, model="embed-english-v3.0", input_type="search_document"
    )

    return CryptoAuditEmbeddingResponse(embeddings=response.embeddings)
