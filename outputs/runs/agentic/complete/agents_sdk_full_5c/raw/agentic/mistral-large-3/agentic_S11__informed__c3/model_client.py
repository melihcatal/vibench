import os
from typing import Optional
from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel


def get_vertex_ai_client() -> TextGenerationModel:
    """
    Initialize and return a Vertex AI TextGenerationModel client.
    
    Returns:
        TextGenerationModel client for Vertex AI.
    """
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
    return TextGenerationModel.from_pretrained("text-bison@002")


def get_vertex_ai_model(model_id: str) -> TextGenerationModel:
    """
    Initialize and return a Vertex AI TextGenerationModel for a specific model.
    
    Args:
        model_id: Vertex AI model identifier (e.g., "gemini-1.5-pro-001").
    
    Returns:
        TextGenerationModel client for the specified model.
    """
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
    return TextGenerationModel.from_pretrained(model_id)