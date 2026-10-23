import os
from google.cloud import aiplatform


def get_vertex_ai_model(project_id: str, location: str, model_name: str):
    """Initializes and returns a Vertex AI GenerativeModel client."""
    aiplatform.init(project=project_id, location=location)
    return aiplatform.preview.language_models.GenerativeModel(model_name)


def get_vertex_ai_embedding_model(project_id: str, location: str, model_name: str):
    """Initializes and returns a Vertex AI TextEmbeddingModel client."""
    aiplatform.init(project=project_id, location=location)
    return aiplatform.TextEmbeddingModel.from_pretrained(model_name)
