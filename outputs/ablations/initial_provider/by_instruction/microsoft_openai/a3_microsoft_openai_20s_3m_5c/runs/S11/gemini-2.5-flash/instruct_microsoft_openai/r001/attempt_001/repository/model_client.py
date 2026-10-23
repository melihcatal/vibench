import os
from openai import OpenAI
from google.cloud import aiplatform

class ModelClient:
    def __init__(self, provider: str):
        self.provider = provider
        self._client = None

    def get_client(self):
        if self._client:
            return self._client

        if self.provider == "openai":
            self._client = OpenAI(
                api_key=os.environ.get("OPENAI_API_KEY"),
                organization=os.environ.get("OPENAI_ORGANIZATION_ID")
            )
        elif self.provider == "google_vertex_ai":
            # For Vertex AI, client initialization often involves project and location
            # and specific services (e.g., aiplatform.gapic.PredictionServiceClient)
            # For simplicity, we'll just initialize the AIPlatform client here.
            project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
            location = os.environ.get("GOOGLE_CLOUD_LOCATION")
            if project_id and location:
                aiplatform.init(project=project_id, location=location)
            self._client = aiplatform
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        return self._client

