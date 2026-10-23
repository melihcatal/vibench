import os
from google.cloud import translate_v3 as translate

def get_translation_client():
    """Initializes and returns the Google Cloud Translation client."""
    return translate.TranslationServiceClient()

def get_gcp_project_id():
    """Retrieves the GCP project ID from an environment variable."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("The GOOGLE_CLOUD_PROJECT environment variable is not set.")
    return project_id
