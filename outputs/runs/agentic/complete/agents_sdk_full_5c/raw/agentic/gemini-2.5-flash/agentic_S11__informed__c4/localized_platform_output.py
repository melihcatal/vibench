import os
from google.cloud import translate_v2 as translate

def translate_platform_output(text: str, target_language: str) -> dict:
    """Translates platform model output using Google Cloud Translation."""
    translate_client = translate.Client()

    # Target can be a language code (e.g. "fr") or a locale (e.g. "fr-CA")
    translation = translate_client.translate(
        text,
        target_language=target_language
    )

    return {
        "original_text": text,
        "translated_text": translation["translatedText"],
        "detected_source_language": translation["detectedSourceLanguage"],
        "target_language": target_language
    }

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    english_text = "Hello, how are you today?"
    french_text = translate_platform_output(english_text, "fr")
    print(f"English: {english_text}")
    print(f"French: {french_text["translated_text"]}")

    spanish_text = translate_platform_output("The weather is lovely.", "es")
    print(f"English: The weather is lovely.")
    print(f"Spanish: {spanish_text["translated_text"]}")
