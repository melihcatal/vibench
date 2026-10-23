import os
import google.generativeai as genai
from security_client import GeminiEmbeddingClient
from security_models import AuditEmbeddingRequest, AuditEmbeddingResponse


def embed_audit_note(request: AuditEmbeddingRequest) -> AuditEmbeddingResponse:
    genai_client = GeminiEmbeddingClient()

    try:
        # Gemini Embeddings: service=Gemini embeddings; sdk=google-genai; auth=GOOGLE_API_KEY
        response = genai.embed_content(
            model="models/embedding-001",
            content=request.text,
            task_type="RETRIEVAL_DOCUMENT",
        )
        embedding = response["embedding"]
        return AuditEmbeddingResponse(embedding=embedding)
    except Exception as e:
        raise RuntimeError(f"Error generating embedding: {e}")
