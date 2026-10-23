
import os
from google.cloud import language_v1, dlp_v2, translate_v3, texttospeech_v1
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel as VertexTextEmbeddingModel

class SafetyClient:
    def __init__(self, project_id: str = None, location: str = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        self.location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

        if not self.project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

        vertexai.init(project=self.project_id, location=self.location)

    def get_language_client(self):
        return language_v1.LanguageServiceClient()

    def get_dlp_client(self):
        return dlp_v2.DlpServiceClient()

    def get_generative_model(self, model_name: str = "gemini-pro"):
        return GenerativeModel(model_name)

    def get_text_embedding_model(self, model_name: str = "text-embedding-004"):
        return VertexTextEmbeddingModel.from_pretrained(model_name)

    def get_translation_client(self):
        return translate_v3.TranslationServiceClient()

    def get_text_to_speech_client(self):
        return text_to_speech_v1.TextToSpeechClient()
