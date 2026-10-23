from google.cloud import language_v1
from google.cloud import dlp_v2
from google.cloud import translate_v3
from google.cloud import texttospeech_v1
import vertexai
from vertexai.language_models import TextEmbeddingModel
from vertexai.preview.generative_models import GenerativeModel


class SafetyClient:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.language_client = language_v1.LanguageServiceClient()
        self.dlp_client = dlp_v2.DlpServiceClient()
        self.translate_client = translate_v3.TranslationServiceClient()
        self.text_to_speech_client = texttospeech_v1.TextToSpeechClient()
        vertexai.init(project=self.project_id, location=self.location)
        self.embedding_model = TextEmbeddingModel.from_pretrained(
            "text-embedding-004"
        )  # Specific Google Cloud Embedding Model
        self.generative_model = GenerativeModel(
            "gemini-1.5-flash-001"
        )  # Specific Google Cloud Generative Model

    def get_language_client(self):
        return self.language_client

    def get_dlp_client(self):
        return self.dlp_client

    def get_translate_client(self):
        return self.translate_client

    def get_text_to_speech_client(self):
        return self.text_to_speech_client

    def get_embedding_model(self):
        return self.embedding_model

    def get_generative_model(self):
        return self.generative_model
