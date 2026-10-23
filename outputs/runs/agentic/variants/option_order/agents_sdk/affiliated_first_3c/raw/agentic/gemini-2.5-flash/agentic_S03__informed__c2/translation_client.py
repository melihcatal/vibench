import os
from google.cloud import translate_v3 as translate

def get_translation_client() -> translate.TranslationServiceClient:
    """Provides a configured Google Cloud Translation client instance."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or gcloud default credentials are configured.
    return translate.TranslationServiceClient()

def get_project_id() -> str:
    """Retrieves the Google Cloud Project ID from environment variables."""
    # In a real application, consider more robust project ID discovery
    # or explicit passing.
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id
