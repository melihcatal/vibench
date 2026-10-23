import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem

def translate_text(text: str, target_language: str = "fr"):
    """
    Translates text to a specified target language using Azure AI Translator.
    
    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "fr", "es", "de").

    Returns:
        The translated text.
    """
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    
    # This is a multi-service endpoint
    endpoint = "https://api.cognitive.microsofttranslator.com"

    credential = AzureKeyCredential(key)
    
    text_translator_client = TextTranslationClient(
        endpoint=endpoint,
        credential=credential,
        region=region
    )

    response = text_translator_client.translate(
        content=[InputTextItem(text=text)],
        to_language=[target_language]
    )
    
    translation = response[0].translations[0]
    return translation.text
