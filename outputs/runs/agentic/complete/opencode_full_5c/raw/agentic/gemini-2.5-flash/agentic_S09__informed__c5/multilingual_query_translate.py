import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    """Translates a query to a target language using Azure AI Translator."""
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    key = os.getenv("AZURE_TRANSLATOR_KEY")

    if not endpoint or not region or not key:
        raise ValueError(
            "AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_REGION or AZURE_TRANSLATOR_KEY environment variables not set."
        )

    client = TextTranslationClient(endpoint, TranslatorCredential(key, region))

    try:
        response = client.translate(
            content=[InputTextItem(text=query)], to=[target_language]
        )
        if response and response[0].translations:
            return response[0].translations[0].text
    except Exception as e:
        print(f"Error translating query: {e}")
    return query  # Return original query on error
