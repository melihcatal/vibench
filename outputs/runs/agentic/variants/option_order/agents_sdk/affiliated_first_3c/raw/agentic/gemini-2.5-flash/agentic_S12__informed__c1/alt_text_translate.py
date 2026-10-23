from google.cloud import translate_v2 as translate
import os

def translate_alt_text(text: str, target_language: str = "es") -> str:
    """Translates generated image descriptions (alt text) using Google Cloud Translation."
    client = translate.Client()

    # Target language can be a language code (e.g., "es" for Spanish, "fr" for French)
    result = client.translate(text, target_language=target_language)

    return result['translatedText']

if __name__ == '__main__':
    print("Running alt_text_translate.py example...")
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up for authentication.

    original_text = "A beautiful sunset over the ocean with a few boats in the distance."
    target_lang = "fr"

    try:
        # For a real run, ensure GOOGLE_APPLICATION_CREDENTIALS is configured.
        # This example will run even without credentials but will likely fail at the API call.
        translated_text = translate_alt_text(original_text, target_language=target_lang)
        print(f"Original ({original_text})")
        print(f"Translated ({target_lang}): {translated_text}")
    except Exception as e:
        print(f"Error during translation: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set or you are authenticated.")
