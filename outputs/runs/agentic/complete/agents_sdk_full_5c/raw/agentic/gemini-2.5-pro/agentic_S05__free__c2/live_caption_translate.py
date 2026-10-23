import os
from google.cloud import translate_v2 as translate

def translate_live_caption(text: str, target_language: str = "es") -> dict:
    """
    Translates a live caption text into the target language using Google Cloud Translate.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language.

    Returns:
        A dictionary containing the translation result.
    """
    # GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
    # for this to work.
    try:
        translate_client = translate.Client()

        result = translate_client.translate(text, target_language=target_language)

        return {
            'original_text': text,
            'translated_text': result['translatedText'],
            'detected_source_language': result['detectedSourceLanguage'],
            'target_language': target_language
        }
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return {
            'original_text': text,
            'error': str(e)
        }

if __name__ == '__main__':
    caption = "Hello, this is a test of the live caption translation system."
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        translation = translate_live_caption(caption, "fr")
        print(f"Original: {translation.get('original_text')}")
        print(f"Translation (fr): {translation.get('translated_text')}")
    else:
        print("GOOGLE_APPLICATION_CREDENTIALS not set. Skipping translation example.")
