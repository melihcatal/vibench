from google.cloud import translate_v3beta1 as translate

def get_translation_client():
    """Provides a configured Google Cloud Translation client.

    Returns:
        A Google Cloud Translation ServiceClient instance.
    """
    # The client will automatically pick up credentials from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS environment variable).
    return translate.TranslationServiceClient()
