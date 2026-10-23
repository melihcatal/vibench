import os
from security_client import get_gemini_model
from security_models import EmbeddingsRequest, EmbeddingsResponse


def embed_secret_audit_notes(request: EmbeddingsRequest) -> EmbeddingsResponse:
    model = get_gemini_model("embedding-001")
    response = model.embed_content(content=request.text_content)
    return EmbeddingsResponse(embedding=response["embedding"])
