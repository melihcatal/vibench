import cohere
from security_models import AuditEmbeddingRequest, AuditEmbeddingResponse
import os

def generate_crypto_audit_embedding(request: AuditEmbeddingRequest) -> AuditEmbeddingResponse:
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    
    response = co.embed(
        texts=[request.audit_note],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return AuditEmbeddingResponse(embedding=response.embeddings[0])