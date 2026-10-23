from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
import os
from typing import Dict, Any

key = os.getenv("AZURE_TRANSLATOR_KEY")
region = os.getenv("AZURE_TRANSLATOR_REGION")
client = TextTranslationClient(credential=TranslatorCredential(key, region))


def payload_translate(text: str, target_language: str) -> str:
    input_text_elements = [InputTextItem(text=text)]
    response = client.translate(content=input_text_elements, to=[target_language])
    translation = response[0] if response else None
    return translation.translations[0].text if translation else text
