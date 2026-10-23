import os
from typing import Dict, Optional
from google.cloud import aiplatform
from google.auth import credentials as google_auth_credentials


def resolve_model_resource(
    model_identifier: Optional[str] = None,
    location: str = "us-central1",
    project_id: Optional[str] = None,
) -> Dict[str, str]:
    """Resolve a Vertex AI model resource by identifier or default."""
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")
    
    aiplatform.init(project=project_id, location=location)
    
    if model_identifier:
        model = aiplatform.Model(model_name=model_identifier)
        model_resource = model.resource_name
    else:
        # Default to a known Vertex AI model
        model_resource = f"projects/{project_id}/locations/{location}/publishers/google/models/gemini-1.5-pro-001"
    
    return {
        "model_resource": model_resource,
        "model_id": model_resource.split("/")[-1],
        "project_id": project_id,
        "location": location,
    }