from typing import List
from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, TranslationResponse

def batch_translate(request: BatchTranslationRequest) -> List[TranslationResponse]:
    """
    Translates a list of text strings using Google Cloud Translation.

    Args:
        request: A BatchTranslationRequest object containing the texts and languages.

    Returns:
        A list of TranslationResponse objects, preserving the original order.
    """
    client = get_translation_client()
    
    results = client.translate(
        request.texts,
        target_language=request.target_language,
        source_language=request.source_language if request.source_language != "auto" else ""
    )
    
    responses = [
        TranslationResponse(
            translated_text=result['translatedText'],
            detected_source_language=result.get('detectedSourceLanguage', 'N/A'),
            original_text=result['input']
        )
        for result in results
    ]
    
    return responses
