from google.cloud import translate_v2 as translate
import os

def translate_alt_text(text: str, target_language: str = "es") -> str:
    """Translates generated image descriptions using Google Cloud Translation."""
    client = translate.Client()

    # Target language can be a language code (e.g. "es" for Spanish, "fr" for French)
    translation = client.translate(text, target_language=target_language)

    return translation['translatedText']

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    english_description = "A fluffy cat sitting on a couch."
    spanish_description = translate_alt_text(english_description, target_language="es")
    print(f"English: {english_description}")
    print(f"Spanish: {spanish_description}")

    french_description = translate_alt_text(english_description, target_language="fr")
    print(f"French: {french_description}")
