import os
from typing import Dict, Any
from google.cloud import aiplatform
from model_models import ModelOutputWithMetadata


def collect_vertex_ai_metadata(
    response: Any,
    model_id: str,
    project: Optional[str] = None,
    location: Optional[str] = None,
) -> ModelOutputWithMetadata:
    """
    Collect model output and platform metadata from a Vertex AI response.
    
    Args:
        response: Raw response object from Vertex AI prediction.
        model_id: Vertex AI model identifier (e.g., "gemini-1.5-pro-001").
        project: Google Cloud project ID. Defaults to environment variable.
        location: Google Cloud region. Defaults to environment variable.
    
    Returns:
        ModelOutputWithMetadata containing text output and provider metadata.
    """
    aiplatform.init(
        project=project or os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
    
    model = aiplatform.Model(model_name=model_id)
    
    metadata = {
        "provider": "vertex_ai",
        "model_id": model.name,
        "model_display_name": model.display_name,
        "project": project or os.getenv("GOOGLE_CLOUD_PROJECT"),
        "location": location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        "usage": {
            "input_tokens": response._prediction_response.metadata.get("inputTokenCount", 0),
            "output_tokens": response._prediction_response.metadata.get("outputTokenCount", 0),
        },
        "safety_ratings": response._prediction_response.metadata.get("safetyRatings", []),
    }
    
    return ModelOutputWithMetadata(
        output=response.text,
        metadata=metadata,
    )