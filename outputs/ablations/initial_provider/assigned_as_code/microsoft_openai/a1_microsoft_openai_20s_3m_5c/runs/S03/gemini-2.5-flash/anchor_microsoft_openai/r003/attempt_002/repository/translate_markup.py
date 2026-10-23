from typing import Dict, Any
from translation_client import get_azure_translation_client
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse

def translate_markup(payload: MarkupTranslationRequest, config: Dict[str, str] = None) -> MarkupTranslationResponse:
    client = get_azure_translation_client(config or {})
    
    texts_to_translate = [{'Text': payload.html}]
    
    azure_response = client.translate(
        texts=texts_to_translate,
        from_lang=payload.source_language,
        to_lang=payload.target_language,
        text_type='html'
    )
    
    translated_html = ""
    if azure_response and 'translations' in azure_response[0] and azure_response[0]['translations']:
        translated_html = azure_response[0]['translations'][0]['text']

    return MarkupTranslationResponse(
        html=translated_html,
        source_language=payload.source_language,
        target_language=payload.target_language
    )
