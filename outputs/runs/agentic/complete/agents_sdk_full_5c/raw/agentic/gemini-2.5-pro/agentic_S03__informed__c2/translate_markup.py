from translation_client import get_translation_client
from translation_models import TranslationResponse

def translate_html(
    html_content: str, target_language: str, source_language: str = None
) -> TranslationResponse:
    """
    Translates HTML content while preserving markup.

    Args:
        html_content: An HTML string.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language. Optional.

    Returns:
        A TranslationResponse object with the translated HTML content.
    """
    client = get_translation_client()

    result = client.translate(
        html_content,
        target_language=target_language,
        source_language=source_language or '',
        mime_type='text/html'
    )

    return TranslationResponse(
        translated_text=result['translatedText'],
        detected_source_language=result.get('detectedSourceLanguage'),
        original_text=result['input']
    )
