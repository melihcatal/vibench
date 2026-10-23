import os
from typing import List
from embeddings_client import EmbeddingsClient
from embeddings_models import BatchTextEmbeddingResponse


def generate_batch_embeddings(texts: List[str]) -> BatchTextEmbeddingResponse:
    """Generates embeddings for a batch of texts using Vertex AI."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = EmbeddingsClient(project_id=project_id, location=location)
    batch_embedding_response = client.embed_batch(texts)
    return batch_embedding_response
