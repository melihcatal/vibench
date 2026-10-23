from google.cloud import translate_v2 as translate
import os

def translate_payload_text(text: str, target_language: str = "es", source_language: str = "en") -> dict:
    """Translates customer-facing message payload text using Google Cloud Translation API."""
    client = translate.Client()

    # Target language can be a language code (e.g. "es") or an ISO 639-1 identifier (e.g. "Spanish")
    result = client.translate(text, target_language=target_language, source_language=source_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }

if __name__ == "__main__":
    # This requires GOOGLE_APPLICATION_CREDENTIALS to be set up or run in a GCP environment.
    # For local testing, ensure your environment is authenticated.
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    test_text = "Hello, how are you today?"
    spanish_translation = translate_payload_text(test_text, target_language="es")
    print(f"Spanish Translation: {spanish_translation}")

    french_translation = translate_payload_text(test_text, target_language="fr")
    print(f"French Translation: {french_translation}")

    japanese_translation = translate_payload_text("Good morning", target_language="ja")
    print(f"Japanese Translation: {japanese_translation}")
