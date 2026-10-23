from google.cloud import aiplatform
import os

def get_vertex_ai_prediction_client(location: str):
    """Provides a configured Vertex AI PredictionServiceClient."""
    # Provider-identifying signal: google.cloud.aiplatform.PredictionServiceClient
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    return aiplatform.PredictionServiceClient(client_options=client_options)

def get_vertex_ai_publisher_model_client(location: str):
    """Provides a configured Vertex AI PredictionServiceClient for publisher models (v1beta1)."""
    # Provider-identifying signal: google.cloud.aiplatform.PredictionServiceClient
    # For streaming and newer models (like Gemini), often the v1beta1 API is used.
    # The client can be instantiated similarly but methods would be from v1beta1.
    # For this helper, we'll keep it simple and assume the main PredictionServiceClient is sufficient
    # or that specific v1beta1 clients are imported where needed (as in stream_platform_generation.py).
    # If a specific v1beta1 client factory is needed, it would look similar:
    # from google.cloud.aiplatform_v1beta1 import PredictionServiceClient as BetaPredictionServiceClient
    # return BetaPredictionServiceClient(client_options=client_options)
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    return aiplatform.PredictionServiceClient(client_options=client_options)


# Example of how configuration might be loaded
def get_project_location_model_config():
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    model_id = os.environ.get("GCP_MODEL_ID", "gemini-pro")
    return project_id, location, model_id

if __name__ == '__main__':
    project, location, model = get_project_location_model_config()
    print(f"Config Loaded: Project={project}, Location={location}, Model={model}")
    client = get_vertex_ai_prediction_client(location)
    print(f"Vertex AI client created: {client.__class__.__name__}")
