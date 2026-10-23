import os
from google.cloud import translate_v2 as translate
from google.api_core.exceptions import GoogleAPICallError

def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates user-facing document fields using Google Cloud Translation API.
    
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set in the environment.

    :param text: The text to translate.
    :param target_language: The ISO 639-1 code for the target language.
    :return: The translated text.
    """
    try:
        # The client automatically uses credentials from the environment.
        translate_client = translate.Client()

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        result = translate_client.translate(text, target_language=target_language)
        
        return result["translatedText"]

    except GoogleAPICallError as e:
        print(f"Google Cloud Translation API error: {e}")
        raise
    except FileNotFoundError:
        print("Google Cloud credentials file not found. Set GOOGLE_APPLICATION_CREDENTIALS.")
        raise
