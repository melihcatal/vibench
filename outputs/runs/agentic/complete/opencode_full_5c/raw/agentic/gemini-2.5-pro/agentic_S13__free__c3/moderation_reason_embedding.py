from safety_client import get_cohere_client
from safety_models import (
    ModerationReasonEmbeddingRequest,
    ModerationReasonEmbeddingResponse,
)


def embed_moderation_reasons(
    request: ModerationReasonEmbeddingRequest,
) -> ModerationReasonEmbeddingResponse:
    client = get_cohere_client()
    response = client.embed(
        texts=request.reasons, model="embed-english-v3.0", input_type="search_document"
    )
    return ModerationReasonEmbeddingResponse(embeddings=response.embeddings)
