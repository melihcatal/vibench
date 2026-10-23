import os
from google.cloud import translate_v3 as translate

def get_translation_client():
    # It's assumed that GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or equivalent default authentication is set up for Google Cloud SDK.
    return translate.TranslationServiceClient()
