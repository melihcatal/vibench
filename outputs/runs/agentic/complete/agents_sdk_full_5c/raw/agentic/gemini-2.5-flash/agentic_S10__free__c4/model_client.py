import vertexai
from vertexai.preview.language_models import TextGenerationModel, TextEmbeddingModel
from vertexai.generative_models import GenerativeModel
import os

class ModelClient:
    def __init__(self):
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
        vertexai.init(project=project_id, location=location)
        
        self._text_model = TextGenerationModel.from_pretrained("text-bison@001")
        self._embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
        self._gemini_model = GenerativeModel("gemini-pro")

    def get_text_generation_model(self):
        return self._text_model

    def get_text_embedding_model(self):
        return self._embedding_model

    def get_gemini_model(self):
        return self._gemini_model
