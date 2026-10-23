from translation_client import AzureTranslatorClient
from translation_models import MarkupTranslationRequest, TranslationResponse
import os

def translate_markup(payload, config=None):
    config = config or {}
    client = AzureTranslatorClient(api_key=config.get('api_key'), region=config.get('region'))

    request_model = MarkupTranslationRequest(
        html_content=payload['html_content'],
        source_language=payload['source_language'],
        target_language=payload['target_language']
    )

    azure_response = client.translate_request(
        text_entries=request_model.to_azure_input(),
        from_lang=request_model.source_language,
        to_lang=request_model.target_language,
        text_type='html'
    )

    response_model = TranslationResponse(
        azure_response=azure_response,
        source_language=request_model.source_language,
        target_language=request_model.target_language
    )

    return {
        'translated_html': response_model.translated_text,
        'source_language': response_model.source_language,
        'target_language': response_model.target_language
    }
