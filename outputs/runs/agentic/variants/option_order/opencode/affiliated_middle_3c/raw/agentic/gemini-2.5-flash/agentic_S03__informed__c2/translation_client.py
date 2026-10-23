from google.cloud import translate_v3 as translate


def get_translation_client():
    """
    Provides a configured Google Cloud Translation client.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    return translate.TranslationServiceClient()
