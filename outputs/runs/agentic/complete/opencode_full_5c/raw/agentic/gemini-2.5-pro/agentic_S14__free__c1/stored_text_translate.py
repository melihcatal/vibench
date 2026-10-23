from google.cloud import translate_v2 as translate
from storage_models import TranslationResponse


def stored_text_translate(text: str, target_language: str) -> TranslationResponse:
    """
    Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., 'en', 'es').

    Returns:
        A TranslationResponse object containing the translated text.
    """
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    response = TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result["detectedSourceLanguage"],
    )

    print(f"Text: {text}")
    print(f"Translation: {response.translated_text}")
    print(f"Detected source language: {response.detected_source_language}")

    return response
