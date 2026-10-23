import os
import vertexai

def get_vertex_client():
    """Initializes the Vertex AI client."""
    # Project and location can be configured through environment variables
    # GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    vertexai.init(project=project_id, location=location)
    return vertexai

