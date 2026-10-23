from google.cloud import aiplatform
from google.cloud.aiplatform_v1beta1 import PredictionServiceClient as BetaPredictionServiceClient # For streaming ops
from google.cloud.aiplatform_v1 import PredictionServiceClient as V1PredictionServiceClient # For general ops
from typing import Optional

class ModelClientConfig:
    def __init__(self, project_id: str, location: str, api_endpoint: Optional[str] = None):
        self.project_id = project_id
        self.location = location
        self.api_endpoint = api_endpoint if api_endpoint else f"{location}-aiplatform.googleapis.com"

def get_vertex_ai_v1_client(config: ModelClientConfig) -> V1PredictionServiceClient:
    """Initializes and returns a Google Cloud Vertex AI V1 PredictionServiceClient."""
    aiplatform.init(project=config.project_id, location=config.location)
    client_options = {"api_endpoint": config.api_endpoint}
    return V1PredictionServiceClient(client_options=client_options)

def get_vertex_ai_beta_client(config: ModelClientConfig) -> BetaPredictionServiceClient:
    """Initializes and returns a Google Cloud Vertex AI V1beta1 PredictionServiceClient (for streaming)."""
    aiplatform.init(project=config.project_id, location=config.location)
    client_options = {"api_endpoint": config.api_endpoint}
    return BetaPredictionServiceClient(client_options=client_options)


if __name__ == '__main__':
    # Example Usage
    # Replace with your actual project_id and location
    config = ModelClientConfig("your-gcp-project-id", "us-central1")
    
    v1_client = get_vertex_ai_v1_client(config)
    print(f"Initialized Vertex AI V1 client: {v1_client.__class__.__name__}")

    beta_client = get_vertex_ai_beta_client(config)
    print(f"Initialized Vertex AI Beta client: {beta_client.__class__.__name__}")
