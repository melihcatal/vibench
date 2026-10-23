from translation_client import get_translation_client
from translation_models import TranslationResponse

def translate_text(text: str, target_language: str, source_language: str = None) -> TranslationResponse:
    """
    Translates a single string of text.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language. Optional.

    Returns:
        A TranslationResponse object containing the translated text.
    """
    client = get_translation_client()

    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language or '',
    )

    return TranslationResponse(
        translated_text=result['translatedText'],
        detected_source_language=result.get('detectedSourceLanguage'),
        original_text=result['input']
    )
