from safety_models import EmbeddingRequest, EmbeddingResponse
from safety_client import embed_text_with_openai


def embed_moderation_reason(text: str) -> EmbeddingResponse:
    request = EmbeddingRequest(text=text)
    response = embed_text_with_openai(request)
    return response
