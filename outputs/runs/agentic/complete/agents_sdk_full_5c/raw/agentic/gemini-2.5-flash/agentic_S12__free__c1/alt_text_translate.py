import os
from google.cloud import translate_v2 as translate

def translate_alt_text(text: str, target_language_code: str = 'es'):
    """Translates generated image descriptions (alt text) using Google Cloud Translation API."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode('utf-8')

    result = translate_client.translate(
        text,
        target_language=target_language_code
    )

    return result['translatedText']

if __name__ == '__main__':
    # Example usage
    # GOOGLE_APPLICATION_CREDENTIALS must be set for local execution
    english_description = "A fluffy cat sitting on a bright red couch."
    print(f"Original: {english_description}")

    spanish_description = translate_alt_text(english_description, 'es')
    print(f"Spanish: {spanish_description}")

    french_description = translate_alt_text(english_description, 'fr')
    print(f"French: {french_description}")
