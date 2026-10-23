from translation_client import get_translate_client
from translation_models import TranslationText, TargetLanguage, SourceLanguage, TranslationResponse

def translate_markup(markup_text: TranslationText, target_language: TargetLanguage, source_language: SourceLanguage = None) -> TranslationResponse:
    """Translates HTML or other markup while preserving tags using Google Cloud Translation.

    Args:
        markup_text: The HTML or markup string to translate.
        target_language: The language to translate the markup into.
        source_language: The language of the input markup. If not specified,
                         Google Cloud Translation will attempt to detect the source language.

    Returns:
        A TranslationResponse object containing the translated markup and the detected source language.
    """
    client = get_translate_client()

    if source_language:
        result = client.translate(markup_text, target_language=target_language, source_language=source_language, format='html')
    else:
        result = client.translate(markup_text, target_language=target_language, format='html')

    return TranslationResponse(
        translated_text=result['translatedText'],
        detected_source_language=result.get('detectedSourceLanguage')
    )
