from google.cloud import translate_v3 as translate
import os


def get_translation_client():
    """Initializes and returns a Google Cloud Translation V3 client."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    
    # The client uses Application Default Credentials for authentication.
    client = translate.TranslationServiceClient()
    return client, f"projects/{project_id}"
