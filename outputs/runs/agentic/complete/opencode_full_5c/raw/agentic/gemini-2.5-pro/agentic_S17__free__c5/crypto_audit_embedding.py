import google.generativeai as genai
from security_client import configure_generative_ai
from security_models import EmbeddingRequest, EmbeddingResponse


def embed_crypto_audit_notes(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embeds crypto audit notes for semantic search using Google Generative AI."""
    configure_generative_ai()

    result = genai.embed_content(
        model="models/embedding-001",
        content=request.content,
        task_type="RETRIEVAL_DOCUMENT",
        title="Crypto Audit Note",
    )

    return EmbeddingResponse(embedding=result["embedding"])
