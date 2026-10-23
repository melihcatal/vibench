import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

def translate_compliance_note(text: str, target_language: str = "en") -> dict:
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION") # Required for multi-service key

    if not all([endpoint, key, region]):
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set.")

    client = TextTranslationClient(endpoint, TranslatorCredential(key, region))

    input_text_items = [InputTextItem(text=text)]
    response = client.translate(content=input_text_items, to=[target_language])

    translations = []
    for translated_text_item in response:
        for translation in translated_text_item.translations:
            translations.append({"language": translation.to, "translated_text": translation.text})

    return {"translations": translations}

