import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient

def translate_markup(markup: str, source_lang: str, target_lang: str) -> str:
    """
    Translates HTML or markup while preserving tags using Azure Translator.
    """
    key = os.getenv('AZURE_TRANSLATOR_KEY')
    endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com')
    if not key:
        raise ValueError("AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_ENDPOINT environment variables are required.")
    credential = AzureKeyCredential(key)
    client = TextTranslationClient(endpoint, credential)
    response = client.translate(
        content=markup,
        content_type="text/html",
        source_language=source_lang,
        target_language=target_lang
    )
    return response[0].translations[0].text