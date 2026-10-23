import os
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel


def get_embeddings_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us-central1"
    aiplatform.init(project=project_id, location=location)
    client = TextEmbeddingModel.from_pretrained("text-embedding-004")
    return client
