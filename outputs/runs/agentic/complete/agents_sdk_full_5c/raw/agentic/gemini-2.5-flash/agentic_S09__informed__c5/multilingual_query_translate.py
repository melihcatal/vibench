import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

def translate_query(text: str, target_language: str = "en") -> str:
    """Translates queries before multilingual embedding search using Azure AI Translator."""
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT") # Note: The prompt mentioned AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION, but the SDK expects endpoint and key.
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not endpoint or not key or not region:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION must be set.")

    client = TextTranslationClient(
        endpoint=endpoint,
        credential=TranslatorCredential(key, region)
    )

    request_body = [InputTextItem(text=text)]
    response = client.translate(content=request_body, to=[target_language])

    if response and response[0].translations:
        return response[0].translations[0].text
    return text # Return original text if translation fails

