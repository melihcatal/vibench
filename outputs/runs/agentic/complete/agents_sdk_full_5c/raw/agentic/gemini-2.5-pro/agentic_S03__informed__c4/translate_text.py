from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_text(request: TranslationRequest) -> TranslationResponse:
    """
    Translates a single text string using Google Cloud Translation.

    Args:
        request: A TranslationRequest object containing the text and languages.

    Returns:
        A TranslationResponse object with the translated text.
    """
    client = get_translation_client()
    
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language if request.source_language != "auto" else ""
    )
    
    return TranslationResponse(
        translated_text=result['translatedText'],
        detected_source_language=result.get('detectedSourceLanguage', 'N/A'),
        original_text=result['input']
    )
