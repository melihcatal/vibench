import os
from google.cloud import translate_v2 as translate

def translate_text(target_language: str, text: str) -> dict:
    """Translates text into the target language.

    Args:
        target_language: The language to translate to (e.g., "fr" for French).
        text: The text to translate.

    Returns:
        A dictionary containing the translated text and the detected source language.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or authentication is handled.
    # For demonstration, assuming credentials are set up.
    # Instantiates a client
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target_language)

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
    }

if __name__ == "__main__":
    # Example usage:
    text_to_translate = "Hello, how are you?"
    target_lang = "es"  # Translate to Spanish

    print(f"Translating: '{text_to_translate}' to '{target_lang}'")
    translation_result = translate_text(target_lang, text_to_translate)
    print(f"Translated text: {translation_result["translated_text"]}")
    print(f"Detected source language: {translation_result["detected_source_language"]}")

    text_to_translate_french = "Bonjour, comment ça va?"
    target_lang_english = "en" # Translate to English

    print(f"\nTranslating: '{text_to_translate_french}' to '{target_lang_english}'")
    translation_result_2 = translate_text(target_lang_english, text_to_translate_french)
    print(f"Translated text: {translation_result_2["translated_text"]}")
    print(f"Detected source language: {translation_result_2["detected_source_language"]}")
