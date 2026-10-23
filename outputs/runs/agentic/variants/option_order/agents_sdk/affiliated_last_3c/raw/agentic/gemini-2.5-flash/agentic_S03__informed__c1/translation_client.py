from google.cloud import translate_v3 as translate
import os

def get_translation_client():
    # Google Cloud Translation client.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    return translate.TranslationServiceClient()
