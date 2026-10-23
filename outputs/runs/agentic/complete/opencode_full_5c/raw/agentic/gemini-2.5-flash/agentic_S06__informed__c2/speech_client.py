import os
from google.cloud import texttospeech
from google.cloud import translate_v3 as translate
import google.generativeai as genai
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
import speech_v1p1beta1 as speech


def get_text_to_speech_client():
    """Provides a Google Cloud Text-to-Speech client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is used for authentication
    return texttospeech.TextToSpeechClient()


def get_translate_client():
    """Provides a Google Cloud Translation client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is used for authentication
    return translate.TranslationServiceClient()


def configure_gemini_embeddings():
    """Configures the Google Gemini Embeddings API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def get_azure_content_safety_client():
    """Provides an Azure AI Content Safety client."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))


def get_speech_to_text_client():
    """Provides a Google Cloud Speech-to-Text client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is used for authentication
    return speech.SpeechClient()
