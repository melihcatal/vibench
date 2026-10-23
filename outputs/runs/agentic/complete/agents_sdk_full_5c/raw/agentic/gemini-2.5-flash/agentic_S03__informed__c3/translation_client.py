import os
from google.cloud import translate_v3

def get_translation_client():
    """Returns a Google Cloud Translation V3 client."""
    return translate_v3.TranslationServiceClient()

def get_project_id():
    """Returns the Google Cloud Project ID from environment variable."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return project_id
