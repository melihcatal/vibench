import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel


class VertexAIClient:
    def __init__(self, project_id: str = None, location: str = None):
        if project_id is None:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if location is None:
            location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        vertexai.init(project=project_id, location=location)
        self.client = GenerativeModel

    def get_model(self, model_name: str):
        return self.client(model_name)
