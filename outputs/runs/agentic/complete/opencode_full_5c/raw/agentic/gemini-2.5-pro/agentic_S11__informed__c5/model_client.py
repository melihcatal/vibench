import os
import vertexai


def get_vertex_client():
    """Initializes the Vertex AI client."""
    # The SDK uses GOOGLE_APPLICATION_CREDENTIALS environment variable implicitly.
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us-central1")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    vertexai.init(project=project_id, location=location)
    return vertexai
