from typing import List
from google.cloud import translate_v2 as translate
from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(
    request: BatchTranslationRequest,
) -> BatchTranslationResponse:
    """Translates a list of strings."""
    client = get_translation_client()
    
    results = client.translate(
        request.texts,
        target_language=request.target_language,
        source_language=request.source_language,
    )
    
    translated_texts = [result["translatedText"] for result in results]
    detected_languages = [result.get("detectedSourceLanguage") for result in results]
    
    return BatchTranslationResponse(
        translated_texts=translated_texts,
        detected_source_languages=detected_languages
    )
