import os
from embeddings_client import EmbeddingsClient
from embeddings_models import TextEmbeddingResponse


def generate_text_embedding(text: str) -> TextEmbeddingResponse:
    """Generates an embedding vector for a single text string using Vertex AI."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = EmbeddingsClient(project_id=project_id, location=location)
    embedding_response = client.embed_text(text)
    return embedding_response
