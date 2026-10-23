from google.cloud import aiplatform

def get_vertex_ai_client(project_id: str, location: str):
    """Initializes and returns a Google Cloud Vertex AI client."""
    # The concrete provider (Google Cloud Vertex AI) is identified by the `google.cloud.aiplatform` import.
    aiplatform.init(project=project_id, location=location)
    # Depending on the specific service, you might return different clients
    # For predictions, you might use PredictionServiceClient or GenerativeModel
    return aiplatform
