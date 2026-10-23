import os
from typing import List, Dict, Any
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

from messaging_models import TranslationRequest, TranslationResponse

def translate_payload_text(request: TranslationRequest) -> TranslationResponse:
    endpoint = os.environ.get("AZURE_TRANSLATOR_TEXT_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_TEXT_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_TEXT_REGION")

    if not endpoint or not key or not region:
        raise ValueError("AZURE_TRANSLATOR_TEXT_ENDPOINT, AZURE_TRANSLATOR_TEXT_KEY, and AZURE_TRANSLATOR_TEXT_REGION environment variables must be set.")

    client = TextTranslationClient(endpoint=endpoint, credential=TranslatorCredential(key, region))

    input_text_items = [InputTextItem(text=request.text)]

    response = client.translate(
        content=input_text_items,
        to=[request.target_language],
        from_parameter=request.source_language # from_parameter is used because 'from' is a reserved keyword
    )

    if response and response[0].translations:
        translated_text = response[0].translations[0].text
        source_language = response[0].detected_language.language if response[0].detected_language else request.source_language
        return TranslationResponse(translated_text=translated_text, source_language=source_language, target_language=request.target_language)
    else:
        raise Exception("Translation failed or returned no results.")
