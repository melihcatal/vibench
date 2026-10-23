from translation_client import get_translate_client
from translation_models import TranslationText, SourceLanguage, TargetLanguage, TranslationResponse

def translate_text(text: TranslationText, target_language: TargetLanguage, source_language: SourceLanguage = None) -> TranslationResponse:
    """Translates a single text string using Google Cloud Translation.

    Args:
        text: The text string to translate.
        target_language: The language to translate the text into (e.g., "es" for Spanish).
        source_language: The language of the input text (e.g., "en" for English). If not
                         specified, Google Cloud Translation will attempt to detect the source language.

    Returns:
        A TranslationResponse object containing the translated text and the detected source language.
    """
    client = get_translate_client()

    if source_language:
        result = client.translate(text, target_language=target_language, source_language=source_language)
    else:
        result = client.translate(text, target_language=target_language)

    return TranslationResponse(
        translated_text=result['translatedText'],
        detected_source_language=result.get('detectedSourceLanguage')
    )
