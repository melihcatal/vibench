from google.cloud import translate

def get_translation_client():
    """Initializes and returns a Google Cloud Translation V3 client."""
    return translate.TranslationServiceClient()
