import os
from google.cloud import aiplatform

def get_vertex_ai_model_client(project_id: str = None, location: str = None):
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = location or os.environ.get("GOOGLE_CLOUD_LOCATION")

    if not project_id:
        raise ValueError("Google Cloud project ID not provided and GOOGLE_CLOUD_PROJECT env var not set.")
    if not location:
        raise ValueError("Google Cloud location not provided and GOOGLE_CLOUD_LOCATION env var not set.")

    aiplatform.init(project=project_id, location=location)
    return aiplatform
