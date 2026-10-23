import os
from google.cloud import monitoring_v3
from google.cloud import storage
from google.cloud import translate_v3
import google.generativeai as genai


def get_monitoring_client():
    """Returns a Google Cloud Monitoring client."""
    return monitoring_v3.MetricServiceClient()


def get_storage_client():
    """Returns a Google Cloud Storage client."""
    return storage.Client()


def get_translate_client():
    """Returns a Google Cloud Translation client."""
    return translate_v3.TranslationServiceClient()


def get_generative_model(model_name: str = "gemini-pro"):
    """Returns a Google Cloud Generative AI model."""
    # Ensure GOOGLE_API_KEY is set in the environment or authenticated via gcloud
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name)
