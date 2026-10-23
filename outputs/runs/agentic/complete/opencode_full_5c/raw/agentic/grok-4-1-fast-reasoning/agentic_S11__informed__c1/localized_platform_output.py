import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
from typing import Optional


def localized_platform_output(text: str, target_language: str = "fr") -> str:
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION", "global")
    if not key:
        return text
    endpoint = f"https://{region}.api.cognitive.microsofttranslator.com"
    client = TextTranslationClient(endpoint, AzureKeyCredential(key))
    result = client.translate([text], to_language=target_language)
    return result[0].translations[0].text
