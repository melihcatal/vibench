from translation_client import get_translation_client
from translation_models import MarkupTranslationRequest, TranslationResponse

def translate_markup(request: MarkupTranslationRequest) -> TranslationResponse:
    """
    Translates a string containing HTML or other markup, preserving tags.

    Args:
        request: A MarkupTranslationRequest object containing the text, languages, and format.

    Returns:
        A TranslationResponse object with the translated markup.
    """
    client = get_translation_client()
    
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language if request.source_language != "auto" else "",
        format_=request.format
    )
    
    return TranslationResponse(
        translated_text=result['translatedText'],
        detected_source_language=result.get('detectedSourceLanguage', 'N/A'),
        original_text=result['input']
    )
