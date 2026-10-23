
import os
from google.cloud import aiplatform

def get_vertex_ai_client(project_id: str = None, location: str = None):
    """
    Initializes and returns a Google Cloud Vertex AI client.

    Args:
        project_id (str, optional): The Google Cloud project ID. Defaults to
                                    reading from GOOGLE_CLOUD_PROJECT environment variable.
        location (str, optional): The Google Cloud region. Defaults to
                                  reading from GOOGLE_CLOUD_LOCATION environment variable.

    Returns:
        google.cloud.aiplatform.CustomJobServiceClient: The Vertex AI client.
    """
    if not project_id:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not location:
        location = os.getenv("GOOGLE_CLOUD_LOCATION")

    if not project_id or not location:
        raise ValueError("Google Cloud project ID and location must be provided or set in environment variables.")

    aiplatform.init(project=project_id, location=location)
    return aiplatform
