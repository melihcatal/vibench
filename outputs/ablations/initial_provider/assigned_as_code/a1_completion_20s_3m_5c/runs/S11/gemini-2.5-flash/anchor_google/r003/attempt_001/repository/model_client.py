import os
from google import genai

def get_vertex_ai_client(project_id: str, location: str):
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or that gcloud default credentials are configured.
    return genai.Client(vertexai=True, project=project_id, location=location)
