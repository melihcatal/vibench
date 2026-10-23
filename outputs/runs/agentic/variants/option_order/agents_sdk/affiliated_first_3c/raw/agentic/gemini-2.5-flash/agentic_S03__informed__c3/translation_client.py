import os
from google.cloud import translate_v3 as translate

def get_translation_client():
    """Provides a configured Google Cloud Translation client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or rely on gcloud default authentication.
    # The project ID is usually inferred from the credentials or environment.
    return translate.TranslationServiceClient()
