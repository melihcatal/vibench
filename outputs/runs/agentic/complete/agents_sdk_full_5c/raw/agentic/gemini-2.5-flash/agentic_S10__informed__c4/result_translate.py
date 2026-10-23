import os
from google.cloud import translate_v2 as translate
import logging

def translate_text(text: str, target_language_code: str = "es") -> str:
    """
    Translates generated model output using Google Cloud Translation.
    
    Args:
        text: The text to translate.
        target_language_code: The BCP-47 language code to translate the text to. Defaults to "es" (Spanish).
    
    Returns:
        The translated text.
    """
    # Initialize the client. Google Cloud Translation automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials if set up.
    client = translate.Client()

    try:
        result = client.translate(text, target_language=target_language_code)
        translated_text = result["translatedText"]
        source_language = result["detectedSourceLanguage"]
        
        print(f"Original Text ({source_language}): {text}")
        print(f"Translated Text ({target_language_code}): {translated_text}")
        
        return translated_text
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        return f"Translation error: {e}"

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or your Google Cloud SDK is configured for authentication.
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Test with an English text to Spanish
    english_text = "Hello, how are you?"
    translate_text(english_text, "es")

    # Test with an English text to French
    english_text_2 = "The quick brown fox."
    translate_text(english_text_2, "fr")

    # Test with a Spanish text to English (auto-detect source language)
    spanish_text = "¿Cómo estás?"
    translate_text(spanish_text, "en")
