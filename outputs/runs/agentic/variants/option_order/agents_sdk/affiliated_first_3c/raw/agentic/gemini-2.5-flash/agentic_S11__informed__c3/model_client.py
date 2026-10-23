import vertexai
from vertexai.generative_models import GenerativeModel
import os

class VertexAIModelClient:
    def __init__(self, project_id: str = None, location: str = "us-central1"):
        self.project_id = project_id if project_id else os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.location = location
        if not self.project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var not set.")
        vertexai.init(project=self.project_id, location=self.location)

    def get_generative_model(self, model_name: str = "gemini-pro") -> GenerativeModel:
        return GenerativeModel(model_name)

    def get_text_embedding_model(self, model_name: str = "textembedding-gecko@003"):
        # Although not used directly in this set of files, this shows how to get an embedding model
        from vertexai.language_models import TextEmbeddingModel
        return TextEmbeddingModel.from_pretrained(model_name)

