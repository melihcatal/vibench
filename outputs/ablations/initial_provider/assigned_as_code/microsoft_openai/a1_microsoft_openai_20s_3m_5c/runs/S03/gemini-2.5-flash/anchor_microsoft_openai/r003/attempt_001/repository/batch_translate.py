from typing import List, Dict, Any
from translation_client import get_azure_translator_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = get_azure_translator_client()
    
    text_elements = [{'Text': text} for text in request.texts]
    
    azure_response = client.translate(
        text_elements=text_elements,
        source_language=request.source_language,
        target_language=request.target_language
    )

    translated_texts = []
    for item in azure_response:
        if 'translations' in item and item['translations']:
            translated_texts.append(item['translations'][0]['text'])
        else:
            translated_texts.append("") # Handle cases where no translation is returned for an item

    return BatchTranslationResponse(
        translations=translated_texts,
        source_language=request.source_language,
        target_language=request.target_language
    )
