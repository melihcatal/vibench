from translation_client import AzureTranslationClient
from translation_models import TranslationRequest, TranslationResponse, parse_azure_translation_response

def translate_markup(payload: TranslationRequest, config=None) -> TranslationResponse:
    client = AzureTranslationClient(api_key=config.get('api_key'), region=config.get('region'))
    
    translated_data = client.translate(
        text_entries=[payload.text],
        from_lang=payload.source_language,
        to_lang=payload.target_language,
        text_type='html'
    )
    
    translated_text = parse_azure_translation_response(translated_data)[0]

    return TranslationResponse(
        text=translated_text,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
