from google.cloud import aiplatform

def get_vertex_ai_client(project_id: str, location: str):
    """Initializes and returns the Google Vertex AI client.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region.

    Returns:
        None. Initializes the Vertex AI SDK.
    """
    aiplatform.init(project=project_id, location=location)
