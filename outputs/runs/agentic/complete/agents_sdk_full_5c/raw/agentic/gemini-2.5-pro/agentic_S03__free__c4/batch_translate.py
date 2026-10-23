import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
from typing import List

from translation_client import get_azure_translator_credentials

def batch_translate(
    texts: List[str], target_language: str, source_language: str
) -> List[str]:
    """
    Translates a list of strings using Azure Translator Service.

    Args:
        texts: A list of strings to translate.
        target_language: The target language code (e.g., 'fr', 'es').
        source_language: The source language code (e.g., 'en').

    Returns:
        A list of translated strings, in the same order as the input.
    """
    endpoint, key, region = get_azure_translator_credentials()
    
    text_translation_client = TextTranslationClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        region=region
    )

    response = text_translation_client.translate(
        content=texts,
        to=[target_language],
        from_parameter=source_language
    )
    
    if not response or not isinstance(response, list):
        return [""] * len(texts)

    translated_texts = [translation.translations[0].text for translation in response]
    return translated_texts
