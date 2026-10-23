from security_client import get_cohere_client
from security_models import EmbeddingRequest, EmbeddingResponse


def create_audit_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    cohere_client = get_cohere_client()

    response = cohere_client.embed(
        texts=request.texts, model=request.model, input_type="search_document"
    )

    return EmbeddingResponse(embeddings=response.embeddings)
