import os
from google.cloud import translate_v2 as translate

# Provider: Google Cloud Translation
# SDK: google-cloud-translate

def translate_text(text: str, target_language: str = "en") -> str | None:
    """
    Translates the given text to the target language using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.

    :param text: The text to translate.
    :param target_language: The ISO 639-1 code of the target language.
    :return: The translated text, or None on failure.
    """
    try:
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None
