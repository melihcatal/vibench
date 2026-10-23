import os
from google.cloud import translate_v2 as translate

def welcome_translate(text, target_language):
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation API.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Google Cloud Translation API identifies itself through the client library import
    # and project credentials. No explicit API key needed if GOOGLE_APPLICATION_CREDENTIALS is set.
    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']
