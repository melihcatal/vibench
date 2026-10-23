
from google.cloud import translate_v2 as translate
import os

def translate_text(text, target_language, source_language=None):
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        source_language: The language of the input text (e.g., "en" for English).
                         If not specified, the API will attempt to detect the source language.
    Returns:
        The translated text.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For local development, set this to the path of your service account key file.
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    text_to_translate = "Hello, how are you?"
    target_lang = "es"  # Spanish
    source_lang = "en"  # English

    translated_text = translate_text(text_to_translate, target_lang, source_lang)
    print(f"Original text: {text_to_translate}")
    print(f"Translated text ({target_lang}): {translated_text}")

    text_to_translate_auto_detect = "Bonjour, comment ça va?"
    target_lang_auto_detect = "en" # English
    translated_text_auto_detect = translate_text(text_to_translate_auto_detect, target_lang_auto_detect)
    print(f"Original text: {text_to_translate_auto_detect}")
    print(f"Translated text ({target_lang_auto_detect}, auto-detected source): {translated_text_auto_detect}")
