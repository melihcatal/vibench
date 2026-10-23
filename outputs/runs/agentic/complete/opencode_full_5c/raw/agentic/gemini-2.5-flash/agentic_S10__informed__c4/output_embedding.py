from model_client import call_gemini_embed_content
from model_models import EmbeddingRequest, EmbeddingResponse
from typing import List


def embed_output(
    text: str, model_name: str = "models/embedding-001"
) -> EmbeddingResponse:
    request = EmbeddingRequest(text=text, model_name=model_name)
    return call_gemini_embed_content(request)
