from security_client import security_client
from security_models import EmbeddingRequest, EmbeddingResponse


def embed_audit_note(request: EmbeddingRequest) -> EmbeddingResponse:
    response = security_client.gemini_model_embedding.embed_content(
        model=security_client.gemini_model_embedding.model_name, content=request.text
    )
    embedding = response["embedding"]
    return EmbeddingResponse(embedding=embedding)
