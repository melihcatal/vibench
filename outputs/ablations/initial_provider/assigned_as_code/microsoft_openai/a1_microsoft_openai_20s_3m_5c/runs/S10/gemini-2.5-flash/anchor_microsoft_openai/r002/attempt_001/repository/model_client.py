from google.cloud import aiplatform

def get_vertex_ai_text_model_client(project_id: str, location: str):
    """Initializes and returns a Vertex AI text generation model client."""
    aiplatform.init(project=project_id, location=location)
    return aiplatform.gapic.PredictionServiceClient()

def get_vertex_ai_publisher_model_endpoint(model_name: str):
    """Returns the endpoint for a publisher model."""
    return f"projects/google/locations/us-central1/publishers/google/models/{model_name}"

def get_vertex_ai_embedding_model_client(project_id: str, location: str):
    """Initializes and returns a Vertex AI embedding model client."""
    aiplatform.init(project=project_id, location=location)
    return aiplatform.gapic.PredictionServiceClient()
