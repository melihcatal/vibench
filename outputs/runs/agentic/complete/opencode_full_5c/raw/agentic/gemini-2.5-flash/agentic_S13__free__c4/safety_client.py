import os
from google.cloud import language_v2
from google.cloud import dlp_v2
from google.cloud import translate_v3
from google.cloud import texttospeech
import vertexai
from vertexai.preview.generative_models import GenerativeModel  # For moderation_summary
from vertexai.preview.language_models import (
    TextEmbeddingModel,
)  # For moderation_reason_embedding


class SafetyClients:
    """Provides initialized clients for various Google Cloud Safety and AI APIs."""

    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        vertexai.init(project=project_id, location=location)

    def get_language_client(self) -> language_v2.LanguageServiceClient:
        """Returns a Google Cloud Natural Language API client."""
        return language_v2.LanguageServiceClient()

    def get_dlp_client(self) -> dlp_v2.DlpServiceClient:
        """Returns a Google Cloud Data Loss Prevention (DLP) API client."""
        return dlp_v2.DlpServiceClient()

    def get_translate_client(self) -> translate_v3.TranslationServiceClient:
        """Returns a Google Cloud Translation API client."""
        return translate_v3.TranslationServiceClient()

    def get_text_to_speech_client(self) -> texttospeech.TextToSpeechClient:
        """Returns a Google Cloud Text-to-Speech API client."""
        return texttospeech.TextToSpeechClient()

    def get_generative_model_client(
        self, model_name: str = "gemini-1.5-flash-001"
    ) -> GenerativeModel:
        """Returns a Vertex AI GenerativeModel client."""
        return GenerativeModel(model_name)

    def get_embedding_model_client(
        self, model_name: str = "text-embedding-004"
    ) -> TextEmbeddingModel:
        """Returns a Vertex AI TextEmbeddingModel client."""
        return TextEmbeddingModel.from_pretrained(model_name)


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID."
        )
    else:
        clients = SafetyClients(project_id)
        print("SafetyClients initialized successfully.")

        # Example: Get a Natural Language client
        lang_client = clients.get_language_client()
        print(f"Natural Language Client: {type(lang_client)}")

        # Example: Get a Generative Model client
        gen_model = clients.get_generative_model_client()
        print(f"Generative Model Client: {type(gen_model)}")
