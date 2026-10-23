from google.cloud import aiplatform

def init_vertex_ai_client(project_id: str, location: str):
    """
    Initializes the Google Cloud Vertex AI client.
    """
    aiplatform.init(project=project_id, location=location)
