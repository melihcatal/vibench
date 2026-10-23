import os
from typing import Optional
import google.cloud.logging
import google.cloud.logging_v2
import google.generativeai as genai
from google.cloud import translate_v3 as translate


def get_gcp_project_id() -> Optional[str]:
    """Retrieves the Google Cloud project ID from environment variables."""
    return os.getenv("GOOGLE_CLOUD_PROJECT_ID")

def get_logging_client() -> google.cloud.logging.Client:
    """Initializes and returns a Google Cloud Logging client."""
    project_id = get_gcp_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return google.cloud.logging.Client(project=project_id)

def get_logging_service_client() -> google.cloud.logging_v2.LoggingServiceV2Client:
    """Initializes and returns a Google Cloud Logging service client (for querying)."""
    return google.cloud.logging_v2.LoggingServiceV2Client()

def get_gemini_model(model_name: str = "gemini-pro") -> genai.GenerativeModel:
    """Initializes and returns a Google Gemini generative model client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set for Gemini API.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def get_translation_client() -> translate.TranslationServiceClient:
    """Initializes and returns a Google Cloud Translation client."""
    project_id = get_gcp_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set for Translation API.")
    return translate.TranslationServiceClient()
