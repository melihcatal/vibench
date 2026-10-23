import os
from google.cloud import kms_v1
import google.generativeai as genai
from google.cloud import translate_v3 as translate

# --- Google Cloud KMS Client Helper ---
def get_kms_client():
    """Returns a Google Cloud KMS client."""
    return kms_v1.KeyManagementServiceClient()

def get_kms_key_path(project_id: str, location_id: str, key_ring_id: str, key_id: str) -> str:
    """Constructs a KMS key path."""
    return get_kms_client().crypto_key_path(project_id, location_id, key_ring_id, key_id)

def get_kms_key_version_path(project_id: str, location_id: str, key_ring_id: str, key_id: str, key_version_id: str) -> str:
    """Constructs a KMS key version path."""
    return get_kms_client().crypto_key_version_path(project_id, location_id, key_ring_id, key_id, key_version_id)

# --- Google Gemini API Client Helper ---
def configure_gemini_api():
    """Configures the Google Gemini API with the API key from environment variables."""
    gemini_api_key = os.environ.get("GOOGLE_API_KEY")
    if not gemini_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set for Gemini API.")
    genai.configure(api_key=gemini_api_key)

def get_gemini_model(model_name: str = "gemini-pro"):
    """Returns a configured Google Gemini model."""
    configure_gemini_api()
    return genai.GenerativeModel(model_name)

# --- Google Cloud Translation Client Helper ---
def get_translate_client():
    """Returns a Google Cloud Translation client."""
    return translate.TranslationServiceClient()

# --- Perspective API Configuration Helper ---
def get_perspective_api_key() -> str:
    """Retrieves the Perspective API key from environment variables."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    return api_key
