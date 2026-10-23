import os
import vertexai
from vertexai.generative_models import GenerativeModel

class ModelClient:
    """A client helper for Vertex AI generative models."""

    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        vertexai.init(project=self.project_id, location=self.location)

    def get_generative_model(self, model_name: str) -> GenerativeModel:
        """Returns an initialized GenerativeModel instance."""
        return GenerativeModel(model_name)

    def get_text_generation_model(self, model_id: str):
        """Returns an initialized TextGenerationModel instance."""
        from vertexai.language_models import TextGenerationModel
        return TextGenerationModel.from_pretrained(model_id)

def get_default_model_client():
    """Provides a default configured ModelClient instance."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return ModelClient(project_id, location)
