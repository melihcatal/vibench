
from google.cloud import translate_v2 as translate
import os

def translate_text(target_language: str, text: str) -> dict:
    """Translates text into the target language using Google Cloud Translation."""
    # Instantiates a client
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Target can be a language code or a language name.
    # E.g. "es", "fr", "ja", "ko", "pt"
    response = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": response["translatedText"],
        "detected_source_language": response["detectedSourceLanguage"],
        "target_language": target_language,
    }

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud credentials environment variable, e.g.:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    onboarding_copy = "Welcome to our platform! We are excited to have you."
    user_locale = "es"  # Example: Spanish

    try:
        translated_result = translate_text(user_locale, onboarding_copy)
        print(f"Original Text: {translated_result['original_text']}")
        print(f"Translated Text ({translated_result['target_language']}): {translated_result['translated_text']}")
        print(f"Detected Source Language: {translated_result['detected_source_language']}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set correctly and the Google Cloud Translation API is enabled for your project.")
