import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_script(
    text: str, target_language: str, source_language: str = None
) -> str:
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    if not endpoint or not key or not region:
        raise RuntimeError(
            "AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION are required"
        )
    client = TextTranslationClient(
        endpoint=endpoint, credential=AzureKeyCredential(key), region=region
    )
    result = client.translate(
        content=[text], to=[target_language], from_parameter=source_language
    )
    return result[0].translations[0].text
