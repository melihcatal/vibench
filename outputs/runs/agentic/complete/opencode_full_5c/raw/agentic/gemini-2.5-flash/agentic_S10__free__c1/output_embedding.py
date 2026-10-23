from typing import List
from model_client import GeminiClient
from model_models import EmbeddingRequest, EmbeddingResponse


def get_output_embedding(
    text: str, model_family: str = "embedding-001"
) -> EmbeddingResponse:
    client = GeminiClient()
    request = EmbeddingRequest(text=text, model_family=model_family)
    return client.embed_text(request)
