import os
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingClient

def get_vertex_client():
    """Initializes and returns the Vertex AI TextEmbeddingClient."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)
    client = TextEmbeddingClient()
    return client
