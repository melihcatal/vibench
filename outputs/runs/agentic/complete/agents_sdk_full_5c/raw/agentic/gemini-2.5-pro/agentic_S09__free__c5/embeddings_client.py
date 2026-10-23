import os
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

def get_embeddings_client() -> TextEmbeddingModel:
    """
    Initializes and returns a Google Vertex AI TextEmbeddingModel client.

    Requires GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables.

    Returns:
        An instance of TextEmbeddingModel.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")

    if not project_id or not location:
        raise ValueError("Please set GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION environment variables.")

    aiplatform.init(project=project_id, location=location)
    
    # Using a specific, identifiable model from Google Vertex AI
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    return model
