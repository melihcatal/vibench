import os
import google.generativeai as genai
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse


def create_audit_embedding(
    request: CryptoAuditEmbeddingRequest,
) -> CryptoAuditEmbeddingResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("embedding-001")  # Using embedding-001 for embeddings

    try:
        response = model.embed_content(
            model="embedding-001", content=request.audit_note
        )
        # Access the embedding from the Embedding object
        embedding_values = response["embedding"]
        return CryptoAuditEmbeddingResponse(embedding=embedding_values)
    except Exception as e:
        raise RuntimeError(
            f"Failed to create embedding with Google Gemini Embeddings: {e}"
        )
