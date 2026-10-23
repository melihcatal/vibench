import os
from typing import Dict, Optional
from google.cloud import aiplatform
from model_models import ModelResource


def select_vertex_ai_model(
    model_display_name: Optional[str] = None,
    model_id: Optional[str] = None,
    project: Optional[str] = None,
    location: Optional[str] = None,
) -> ModelResource:
    """
    Resolve a Vertex AI model resource by display name or ID.
    
    Args:
        model_display_name: Human-readable model name (e.g., "gemini-1.5-pro").
        model_id: Vertex AI model ID (e.g., "gemini-1.5-pro-001").
        project: Google Cloud project ID. Defaults to environment variable.
        location: Google Cloud region. Defaults to environment variable.
    
    Returns:
        ModelResource containing provider-specific model handle and metadata.
    
    Raises:
        ValueError: If neither model_display_name nor model_id is provided.
    """
    if not model_display_name and not model_id:
        raise ValueError("Either model_display_name or model_id must be provided.")
    
    aiplatform.init(
        project=project or os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
    
    if model_id:
        model = aiplatform.Model(model_name=model_id)
    else:
        models = aiplatform.Model.list(filter=f"display_name={model_display_name}")
        if not models:
            raise ValueError(f"No model found with display_name: {model_display_name}")
        model = models[0]
    
    return ModelResource(
        provider="vertex_ai",
        model_handle=model.resource_name,
        model_display_name=model.display_name,
        metadata={
            "model_id": model.name,
            "version": model.version_id,
            "region": location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        },
    )