from security_client import SecurityClients
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse

def embed_audit_notes(request: CryptoAuditEmbeddingRequest) -> CryptoAuditEmbeddingResponse:
    openai_client = SecurityClients.get_openai_client()

    embedding_model = "text-embedding-3-small"

    response = openai_client.embeddings.create(
        input=request.audit_notes,
        model=embedding_model
    )

    embeddings = [data.embedding for data in response.data]

    return CryptoAuditEmbeddingResponse(embeddings=embeddings)
