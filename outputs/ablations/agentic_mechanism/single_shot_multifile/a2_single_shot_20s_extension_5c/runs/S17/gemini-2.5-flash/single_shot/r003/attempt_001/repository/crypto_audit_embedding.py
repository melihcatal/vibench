import os
from security_client import get_openai_client
from security_models import AuditEmbeddingRequest, AuditEmbeddingResponse
from typing import List

def create_audit_embedding(request: AuditEmbeddingRequest) -> AuditEmbeddingResponse:
    openai_client = get_openai_client()
    
    response = openai_client.embeddings.create(
        input=[request.text],
        model="text-embedding-ada-002"
    )
    
    embedding_vector: List[float] = response.data[0].embedding
    
    return AuditEmbeddingResponse(embedding=embedding_vector)
