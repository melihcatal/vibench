import os
from typing import List

from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient


def translate_script(
    text: str, target_language: str, source_language: str = "en"
) -> str:
    """
    Translates a script to a target language using Azure AI Translator.

    Args:
        text: The text to translate.
        target_language: The language to translate the text into (e.g., 'fr').
        source_language: The source language of the text (e.g., 'en').

    Returns:
        The translated text.
    """
    translator_key = os.environ["AZURE_TRANSLATOR_KEY"]
    translator_region = os.environ["AZURE_TRANSLATOR_REGION"]
    endpoint = "https://api.cognitive.microsofttranslator.com/"

    text_translator_client = TextTranslationClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(translator_key),
        region=translator_region,
    )

    response = text_translator_client.translate(
        content=[text], to=[target_language], from_parameter=source_language
    )

    if response and response[0].translations:
        return response[0].translations[0].text
    
    return ""
