from google.cloud import translate

def get_translate_client():
    """Returns a Google Cloud Translation client."""
    return translate.TranslationServiceClient()
