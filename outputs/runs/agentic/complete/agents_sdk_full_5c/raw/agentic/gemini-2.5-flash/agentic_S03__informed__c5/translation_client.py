from google.cloud import translate_v3beta1 as translate
import os

def get_translation_client():
    """Provides a configured Google Cloud Translation client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in the environment
    # or authentication is handled implicitly by the Google Cloud SDK.
    return translate.TranslationServiceClient()
