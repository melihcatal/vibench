import os
import openai
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse


def get_audit_embedding(
    request: CryptoAuditEmbeddingRequest,
) -> CryptoAuditEmbeddingResponse:
    """Embeds crypto audit notes for semantic search using OpenAI Embeddings."""
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # Using a suitable OpenAI embedding model
    model_id = "text-embedding-ada-002"

    response = client.embeddings.create(input=request.audit_note_text, model=model_id)

    embedding_vector = response.data[0].embedding

    return CryptoAuditEmbeddingResponse(embedding_vector=embedding_vector)
