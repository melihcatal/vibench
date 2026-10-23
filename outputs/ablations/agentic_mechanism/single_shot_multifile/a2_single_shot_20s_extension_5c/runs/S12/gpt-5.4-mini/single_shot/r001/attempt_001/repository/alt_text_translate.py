import os
from typing import Optional

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

AZURE_TRANSLATOR_ENDPOINT_ENV = "AZURE_TRANSLATOR_ENDPOINT"
AZURE_TRANSLATOR_KEY_ENV = "AZURE_TRANSLATOR_API_KEY"
AZURE_TRANSLATOR_REGION_ENV = "AZURE_TRANSLATOR_REGION"


def translate_alt_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    endpoint = os.environ.get(AZURE_TRANSLATOR_ENDPOINT_ENV, "").strip()
    key = os.environ.get(AZURE_TRANSLATOR_KEY_ENV, "").strip()
    region = os.environ.get(AZURE_TRANSLATOR_REGION_ENV, "").strip()
    if not endpoint or not key or not region:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_API_KEY, and AZURE_TRANSLATOR_REGION are required")
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)
    kwargs = {"content": [text], "to": [target_language]}
    if source_language:
        kwargs["from_parameter"] = source_language
    result = client.translate(**kwargs)
    return result[0].translations[0].text if result and result[0].translations else text
