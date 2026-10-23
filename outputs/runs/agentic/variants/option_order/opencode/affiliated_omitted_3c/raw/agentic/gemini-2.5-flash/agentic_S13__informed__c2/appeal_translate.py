import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem


def translate_appeal_text(
    text: str, target_language: str, source_language: str = "en"
) -> str:
    """
    Translates appeal text for review using Azure AI Translator.
    Requires AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables.
    """
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not key or not region:
        raise ValueError(
            "AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION must be set in environment variables."
        )

    client = TextTranslationClient(credential=TranslatorCredential(key, region))

    input_text_items = [InputTextItem(text_content=text)]

    response = client.translate(
        content=input_text_items, to=[target_language], from_parameter=source_language
    )

    if response and response[0].translations:
        return response[0].translations[0].text

    return ""
