from security_client import SecurityClient
from security_models import EmbeddingRequest, EmbeddingResponse
import google.generativeai as genai
import os


def embed_audit_note(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embeds crypto audit notes for semantic search using Gemini Embeddings."""
    client = SecurityClient()

    if not client.gemini_embedding_model or not os.getenv("GOOGLE_API_KEY"):
        return EmbeddingResponse(
            embedding=[],
            error="Gemini Embedding API not configured. Please set GOOGLE_API_KEY.",
        )

    # Gemini Embeddings: service=Gemini embeddings; sdk=google-genai; interface=sdk; auth=GOOGLE_API_KEY
    try:
        response = genai.embed_content(
            model=client.gemini_embedding_model,
            content=request.text,
            task_type="RETRIEVAL_DOCUMENT",
        )
        embedding = response["embedding"]
        return EmbeddingResponse(embedding=embedding)
    except Exception as e:
        return EmbeddingResponse(embedding=[], error=str(e))
