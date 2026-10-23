from google.cloud import translate_v2 as translate
import os

def script_translate(text: str, target_language: str) -> str:
    """
    Translates narration scripts using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The language code to translate the text into (e.g., "es" for Spanish).

    Returns:
        The translated text.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"

    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    return result['translatedText']
