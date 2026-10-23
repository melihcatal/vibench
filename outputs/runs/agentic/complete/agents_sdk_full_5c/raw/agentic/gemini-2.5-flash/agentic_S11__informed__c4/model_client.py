import os
import vertexai

class VertexAIModelClient:
    """Local configuration and client helper utilities for Vertex AI."""

    def __init__(self, project_id: str = None, location: str = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable or project_id must be set.")
        
        vertexai.init(project=self.project_id, location=self.location)
    
    def get_generative_model(self, model_name: str):
        from vertexai.preview.generative_models import GenerativeModel
        return GenerativeModel(model_name)

    def get_text_generation_model(self, model_name: str):
        from vertexai.language_models import TextGenerationModel
        return TextGenerationModel.from_pretrained(model_name)

