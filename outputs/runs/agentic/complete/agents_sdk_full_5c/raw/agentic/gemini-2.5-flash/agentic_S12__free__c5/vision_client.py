import os
from google.cloud import vision_v1p4beta1 as vision
from google.cloud import translate_v3 as translate
from google.cloud import storage
import google.generativeai as genai

def get_vision_client():
    """Initializes and returns a Google Cloud Vision API client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set or running in a GCP environment
    return vision.ImageAnnotatorClient()

def get_generative_model(model_name: str = 'gemini-pro'):
    """Initializes and returns a Google Generative AI model client."""
    # Ensure GOOGLE_API_KEY is set in environment variables
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def get_translation_client():
    """Initializes and returns a Google Cloud Translation API client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set or running in a GCP environment
    return translate.TranslationServiceClient()

def get_storage_client():
    """Initializes and returns a Google Cloud Storage client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set or running in a GCP environment
    return storage.Client()

