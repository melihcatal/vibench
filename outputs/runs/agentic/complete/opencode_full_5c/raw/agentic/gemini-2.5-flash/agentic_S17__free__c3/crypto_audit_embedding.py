from security_client import get_embedding_model
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse


def embed_audit_note(
    request: CryptoAuditEmbeddingRequest,
) -> CryptoAuditEmbeddingResponse:
    model = get_embedding_model()

    # The Vertex AI Text Embedding API expects a list of texts
    embeddings = model.get_embeddings([request.audit_note])

    if embeddings and embeddings[0].values:
        return CryptoAuditEmbeddingResponse(embedding=embeddings[0].values)
    else:
        return CryptoAuditEmbeddingResponse(embedding=[])
