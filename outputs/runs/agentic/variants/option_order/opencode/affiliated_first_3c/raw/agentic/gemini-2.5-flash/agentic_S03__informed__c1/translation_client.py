from google.cloud import translate_v3 as translate


def get_translation_client():
    """Returns a Google Cloud Translation V3 client."""
    return translate.TranslationServiceClient()
