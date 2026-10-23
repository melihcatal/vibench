from typing import Dict, Any
from translation_client import get_azure_translator_client
from translation_models import MarkupTranslationRequest, TranslationResponse

def translate_markup(request: MarkupTranslationRequest) -> TranslationResponse:
    client = get_azure_translator_client()

    text_elements = [{'Text': request.markup_text}]

    azure_response = client.translate(
        text_elements=text_elements,
        source_language=request.source_language,
        target_language=request.target_language,
        text_type="html"
    )

    translated_text = ""
    if azure_response and 'translations' in azure_response[0] and azure_response[0]['translations']:
        translated_text = azure_response[0]['translations'][0]['text']

    return TranslationResponse(
        text=translated_text,
        source_language=request.source_language,
        target_language=request.target_language
    )
