import os
from google.cloud import translate_v3


def get_translation_client():
    """Initializes and returns a Google Cloud Translation V3 client."""
    return translate_v3.TranslationServiceClient()


def get_project_id():
    """Returns the Google Cloud Project ID from environment variable."""
    return os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
