from typing import List, Dict, Any
from translation_client import get_azure_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(payload: BatchTranslationRequest, config: Dict[str, str] = None) -> BatchTranslationResponse:
    client = get_azure_translation_client(config or {})
    
    texts_to_translate = [{'Text': text} for text in payload.texts]
    
    azure_response = client.translate(
        texts=texts_to_translate,
        from_lang=payload.source_language,
        to_lang=payload.target_language
    )
    
    translated_texts = []
    for item in azure_response:
        if 'translations' in item and item['translations']:
            translated_texts.append(item['translations'][0]['text'])
        else:
            # Handle cases where translation might not be available for an item
            translated_texts.append("") 

    return BatchTranslationResponse(
        texts=translated_texts,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
