import os
from google.cloud import translate_v2 as translate

def translate_record_field(text: str, target_language: str = 'es') -> str:
    """
    Translates a text field to a specified language using Google Cloud Translate.

    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.

    :param text: The text to translate.
    :param target_language: The ISO 639-1 code for the target language.
    :return: The translated text.
    """
    if not text:
        return ""

    try:
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        print(f"An error occurred with Google Cloud Translate: {e}")
        return f"Translation error: {text}"
