from google.cloud import aiplatform


def get_vertex_ai_model_client(project_id: str, location: str):
    """
    Returns a Vertex AI model client.
    """
    aiplatform.init(project=project_id, location=location)
    return aiplatform.gapic.PredictionServiceClient()
