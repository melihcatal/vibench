import os
from google.cloud import language_v2, dlp_v2, translate_v3, texttospeech_v1
import google.generativeai as genai
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

class SafetyClient:
    """
    Provides client utilities for various Text Content Safety services.
    Initializes clients for Google Cloud APIs and Azure Content Safety.
    """
    _gcp_project_id: str = None

    def __init__(self, gcp_project_id: str = None):
        self._gcp_project_id = gcp_project_id or os.environ.get("GCP_PROJECT_ID")
        if not self._gcp_project_id:
            print("WARNING: GCP_PROJECT_ID not provided. Some Google Cloud clients may not initialize properly.")

        self._language_client = None
        self._dlp_client = None
        self._translate_client = None
        self._text_to_speech_client = None
        self._generative_model = None
        self._embedding_model = None
        self._azure_content_safety_client = None

    def get_google_language_client(self) -> language_v2.LanguageServiceClient:
        if not self._language_client:
            self._language_client = language_v2.LanguageServiceClient()
        return self._language_client

    def get_google_dlp_client(self) -> dlp_v2.DlpServiceClient:
        if not self._dlp_client:
            self._dlp_client = dlp_v2.DlpServiceClient()
        return self._dlp_client
    
    def get_google_translate_client(self) -> translate_v3.TranslationServiceClient:
        if not self._translate_client:
            self._translate_client = translate_v3.TranslationServiceClient()
        return self._translate_client

    def get_google_text_to_speech_client(self) -> texttospeech_v1.TextToSpeechClient:
        if not self._text_to_speech_client:
            self._text_to_speech_client = texttospeech_v1.TextToSpeechClient()
        return self._text_to_speech_client

    def get_google_generative_model(self, model_name: str = "gemini-pro"):
        # Ensure API key is set for Google Generative AI
        if not genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")):
             print("WARNING: GOOGLE_API_KEY environment variable not set for Generative AI.")
        if not self._generative_model:
            self._generative_model = genai.GenerativeModel(model_name)
        return self._generative_model

    def get_google_embedding_model(self, model_name: str = "embedding-001"):
        if not genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")):
             print("WARNING: GOOGLE_API_KEY environment variable not set for Generative AI.")
        if not self._embedding_model:
            self._embedding_model = genai.GenerativeModel(model_name) # Assuming embedding-001 is a GenerativeModel for embeddings
        return self._embedding_model

    def get_azure_content_safety_client(self) -> ContentSafetyClient:
        if not self._azure_content_safety_client:
            endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
            key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
            if not endpoint or not key:
                raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set for Azure Content Safety.")
            self._azure_content_safety_client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        return self._azure_content_safety_client

    @property
    def gcp_project_id(self) -> str:
        if not self._gcp_project_id:
            raise ValueError("Google Cloud Project ID is not set.")
        return self._gcp_project_id

if __name__ == '__main__':
    # Example usage:
    # Set environment variables for testing:
    # os.environ["GCP_PROJECT_ID"] = "your-gcp-project-id"
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "https://your-endpoint.cognitiveservices.azure.com"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "your-key"
    # os.environ["GOOGLE_API_KEY"] = "your-google-api-key"

    client_manager = SafetyClient()

    try:
        lang_client = client_manager.get_google_language_client()
        print(f"Google Language Client: {lang_client.__class__.__name__}")
    except Exception as e:
        print(f"Could not initialize Google Language Client: {e}")

    try:
        azure_client = client_manager.get_azure_content_safety_client()
        print(f"Azure Content Safety Client: {azure_client.__class__.__name__}")
    except ValueError as e:
        print(f"Could not initialize Azure Content Safety Client: {e}")
    except Exception as e:
        print(f"Could not initialize Azure Content Safety Client: {e}")

    try:
        gemini_model = client_manager.get_google_generative_model()
        print(f"Google Generative Model (Gemini): {gemini_model.model_name}")
    except Exception as e:
        print(f"Could not initialize Google Generative Model: {e}")
