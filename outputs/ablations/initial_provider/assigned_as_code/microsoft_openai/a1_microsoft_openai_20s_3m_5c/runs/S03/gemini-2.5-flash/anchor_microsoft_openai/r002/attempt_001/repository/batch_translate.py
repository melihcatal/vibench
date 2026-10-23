from typing import List
from translation_client import AzureTranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse, parse_azure_translation_response


def batch_translate(payload: BatchTranslationRequest, config=None) -> BatchTranslationResponse:
    client = AzureTranslationClient(api_key=config.get('api_key'), region=config.get('region'))
    
    translated_data = client.translate(
        text_entries=payload.texts,
        from_lang=payload.source_language,
        to_lang=payload.target_language
    )
    
    translated_texts = parse_azure_translation_response(translated_data)

    return BatchTranslationResponse(
        translations=translated_texts,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
