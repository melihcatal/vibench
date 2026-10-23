import google.generativeai as genai
from security_client import get_gemini_embedding_model
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse
import os


def create_audit_embedding(
    request: CryptoAuditEmbeddingRequest,
) -> CryptoAuditEmbeddingResponse:
    model_name = get_gemini_embedding_model()
    response = genai.embed_content(
        model=model_name,
        content=request.audit_notes,
        task_type="RETRIEVAL_DOCUMENT",  # Specify task type for better embeddings
    )
    return CryptoAuditEmbeddingResponse(embedding_vector=response["embedding"])
