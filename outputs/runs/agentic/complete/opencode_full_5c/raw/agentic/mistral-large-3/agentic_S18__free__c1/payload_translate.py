from google.cloud import translate_v2 as translate
import os


def payload_translate(text: str, target_language: str = "es") -> Dict[str, Any]:
    """
    Translates customer-facing message payload text using Google Cloud Translation API.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., 'es' for Spanish).

    Returns:
        Dict[str, Any]: Translation results including original and translated text.
    """
    # Initialize Google Cloud Translation client
    translate_client = translate.Client()

    # Translate the text
    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
        "model": "google-cloud-translate-v2",
    }
