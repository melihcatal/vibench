import os
from model_client import VertexAIModelClient
from model_models import EmbeddingRequest, EmbeddingResponse


def embed_output(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embeds model outputs for clustering or retrieval using Vertex AI embedding models."""
    client = (
        VertexAIModelClient()
    )  # Uses google.cloud.aiplatform via VertexAIModelClient

    embeddings = client.generate_embeddings(request.text)

    return EmbeddingResponse(embeddings=embeddings)
