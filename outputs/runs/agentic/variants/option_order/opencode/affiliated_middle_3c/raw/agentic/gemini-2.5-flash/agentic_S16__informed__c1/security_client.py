from google.cloud import secretmanager
import google.generativeai as genai
from google.cloud import translate_v3 as translate
import os


def get_secret_manager_client():
    """
    Provides a configured client for Google Secret Manager.
    Provider: Google Cloud Secret Manager
    """
    return secretmanager.SecretManagerServiceClient()


def get_gemini_model(model_name: str = "gemini-pro"):
    """
    Configures and returns a Gemini model.
    Provider: Google Gemini API
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name)


def get_translation_client():
    """
    Provides a configured client for Google Cloud Translation.
    Provider: Google Cloud Translation
    """
    return translate.TranslationServiceClient()
