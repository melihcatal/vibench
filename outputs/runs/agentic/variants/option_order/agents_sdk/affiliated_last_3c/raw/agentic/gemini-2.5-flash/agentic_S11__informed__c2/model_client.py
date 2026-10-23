import vertexai
import os

def init_vertex_ai_client(project_id: str = None, location: str = None):
    # Use environment variables if not provided
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    location = location or os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    print(f"Vertex AI client initialized for project {project_id} in {location}")
    return True

