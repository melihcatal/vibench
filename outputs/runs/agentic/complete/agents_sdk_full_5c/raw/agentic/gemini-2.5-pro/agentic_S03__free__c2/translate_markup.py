from typing import List
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
from translation_client import AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION

def translate_html(html_string: str, target_language: str, source_language: str) -> str:
    """
    Translates an HTML string while preserving markup using Azure Translator.

    Args:
        html_string: The HTML content to translate.
        target_language: The target language code (e.g., 'fr').
        source_language: The source language code (e.g., 'en').

    Returns:
        The translated HTML string.
    """
    if not all([AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION]):
        raise ValueError("Azure Translator credentials are not set in environment variables.")

    credential = AzureKeyCredential(AZURE_TRANSLATOR_KEY)
    
    text_translator_client = TextTranslationClient(
        region=AZURE_TRANSLATOR_REGION,
        credential=credential
    )

    response = text_translator_client.translate(
        content=[html_string],
        to=[target_language],
        from_parameter=source_language,
        text_type="html"
    )

    if response and len(response) > 0 and response[0].translations:
        return response[0].translations[0].text
    
    return ""
