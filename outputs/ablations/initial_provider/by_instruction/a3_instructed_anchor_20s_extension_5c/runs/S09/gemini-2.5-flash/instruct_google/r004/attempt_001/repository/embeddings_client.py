import os
from google.cloud import aiplatform

class EmbeddingsClient:
    """Provides client utilities for Google Vertex AI Embeddings API.
    """
    def __init__(self, project_id: str = None, location: str = "us-central1", model_id: str = "text-embedding-004"):
        if project_id is None:
            self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
            if not self.project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        else:
            self.project_id = project_id
            
        self.location = location
        self.model_id = model_id
        aiplatform.init(project=self.project_id, location=self.location)
        self.client = aiplatform.gapic.PredictionServiceClient.from_service_account_json(
            os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        )
        self.endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_id}"

    def get_client(self):
        return self.client

    def get_endpoint(self):
        return self.endpoint

    def get_model_id(self):
        return self.model_id
