import os
from google.cloud import translate_v3beta1

def get_translation_client():
    """Initializes and returns a Google Cloud Translation client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return translate_v3beta1.TranslationServiceClient()

def get_project_id():
    """Retrieves the Google Cloud Project ID from the environment variable."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return project_id
