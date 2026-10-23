from safety_client import GoogleCloudClient
from safety_models import ModerationReasonEmbeddingRequest, ModerationReasonEmbeddingResponse

def embed_moderation_reasons(request: ModerationReasonEmbeddingRequest) -> ModerationReasonEmbeddingResponse:
    client = GoogleCloudClient()
    embeddings = client.embed_text(request.reasons)
    return ModerationReasonEmbeddingResponse(embeddings=embeddings)
