import os
from google.cloud import translate_v3 as translate

def get_translation_client():
    """
    Initializes and returns a Google Cloud Translation API client.

    Assumes that the GOOGLE_APPLICATION_CREDENTIALS environment variable
    is set to the path of a valid service account JSON file.
    """
    return translate.TranslationServiceClient()

def get_gcp_project_id():
    """
    Retrieves the GCP project ID from environment variables.
    This is required for making calls to the Google Cloud Translation API.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")
    return project_id
