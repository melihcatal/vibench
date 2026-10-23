from speech_client import get_translation_client
from speech_models import TranslationResponse


def translate_caption(text: str, target_language: str = "es") -> TranslationResponse:
    """
    Translates a live caption text into another language using Google Cloud Translate.

    Args:
        text: The caption text to translate.
        target_language: The target language code (e.g., 'es' for Spanish).

    Returns:
        A TranslationResponse object with the translated text.
    """
    client = get_translation_client()

    result = client.translate(text, target_language=target_language)

    response = TranslationResponse(
        translated_text=result["translatedText"],
        detected_language_code=result.get("detectedSourceLanguage"),
    )
    return response


if __name__ == "__main__":
    caption = "Hello, this is a live test of our translation service."
    translated_response = translate_caption(caption, "fr")
    print(f"Original ('{translated_response.detected_language_code}'): {caption}")
    print(f"Translated ('fr'): {translated_response.translated_text}")
