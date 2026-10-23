
import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation.
    
    Args:
        text: The text to translate.
        target_language: The language to translate to (e.g., "es" for Spanish, "fr" for French).

    Returns:
        The translated text.
    """
    # Google Cloud Translation API setup
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise as per Google Cloud documentation.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    translate_client = translate.Client()

    response = translate_client.translate(
        text,
        target_language=target_language
    )
    
    return response["translatedText"]

if __name__ == "__main__":
    # Example usage:
    text_to_translate = "Hola mundo"
    translated_text = translate_text(text_to_translate, target_language="en")
    print(f"Original text: {text_to_translate}")
    print(f"Translated text (en): {translated_text}")

    text_to_translate_french = "Hello World"
    translated_text_french = translate_text(text_to_translate_french, target_language="fr")
    print(f"Original text: {text_to_translate_french}")
    print(f"Translated text (fr): {translated_text_french}")
