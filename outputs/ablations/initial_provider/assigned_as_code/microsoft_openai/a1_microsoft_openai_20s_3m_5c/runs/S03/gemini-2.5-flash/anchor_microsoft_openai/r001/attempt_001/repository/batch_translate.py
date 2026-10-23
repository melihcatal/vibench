from translation_client import AzureTranslatorClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse
import os

def batch_translate(payload, config=None):
    config = config or {}
    client = AzureTranslatorClient(api_key=config.get('api_key'), region=config.get('region'))

    request_model = BatchTranslationRequest(
        texts=payload['texts'],
        source_language=payload['source_language'],
        target_language=payload['target_language']
    )

    azure_response = client.translate_request(
        text_entries=request_model.to_azure_input(),
        from_lang=request_model.source_language,
        to_lang=request_model.target_language
    )

    response_model = BatchTranslationResponse(
        azure_response=azure_response,
        source_language=request_model.source_language,
        target_language=request_model.target_language
    )

    return {
        'translated_texts': response_model.translated_texts,
        'source_language': response_model.source_language,
        'target_language': response_model.target_language
    }
