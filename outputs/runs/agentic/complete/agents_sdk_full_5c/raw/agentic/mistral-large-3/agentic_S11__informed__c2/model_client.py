import os
from typing import Optional
from google.cloud import aiplatform
from google.auth import credentials as google_auth_credentials


def get_vertex_ai_client(
    location: str = "us-central1",
    project_id: Optional[str] = None,
) -> aiplatform.generative_models.GenerativeModel:
    """Initialize and return a Vertex AI generative model client."""
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")
    
    aiplatform.init(project=project_id, location=location)
    return aiplatform.generative_models