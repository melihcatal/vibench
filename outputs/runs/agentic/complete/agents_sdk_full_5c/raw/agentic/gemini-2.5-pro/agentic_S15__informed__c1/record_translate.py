from google.cloud import translate_v2 as translate
import os

def translate_text(text: str, target_language: str = "en"):
    """

    Translates text into the target language using the Google Cloud Translation API.
    Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'en', 'es').

    Returns:
        The translated text as a string.
    """
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS not set.")

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]
