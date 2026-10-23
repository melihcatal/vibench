import os
import vertexai

def get_client():
    """Initializes the Vertex AI client."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")
        
    vertexai.init(project=project_id, location=location)
    return vertexai

