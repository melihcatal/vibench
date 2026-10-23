import os
from typing import List
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem


async def translate_captions(
    text_chunks: List[str], target_language: str = "es"
) -> List[str]:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not endpoint or not key or not region:
        raise ValueError(
            "AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set."
        )

    # Provider-specific: Azure AI Translator SDK
    client = TextTranslationClient(
        endpoint=endpoint, credential=TranslatorCredential(key, region)
    )

    input_text_items = [InputTextItem(text=chunk) for chunk in text_chunks]
    response = await client.translate_async(
        content=input_text_items, to=[target_language]
    )

    translated_texts = []
    for translated_text_item in response:
        for translation in translated_text_item.translations:
            translated_texts.append(translation.text)
    return translated_texts
