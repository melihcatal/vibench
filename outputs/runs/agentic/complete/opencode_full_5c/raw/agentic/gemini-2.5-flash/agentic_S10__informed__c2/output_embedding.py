import os
from typing import List, Union

from model_client import GeminiClient
from model_models import EmbeddingRequest, EmbeddingResponse


def embed_output(
    text: Union[str, List[str]], model_name: str = "embedding-001"
) -> EmbeddingResponse:
    """Embeds model outputs for clustering or retrieval using Gemini Embeddings."""
    client = GeminiClient()
    request = EmbeddingRequest(
        text=text,
        model_name=model_name,
    )
    response = client.embed_content(request)
    return response
