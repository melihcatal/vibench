from __future__ import annotations

from typing import Dict

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_customer_payload(text: str, endpoint: str, key: str, target_language: str = "es") -> Dict[str, str]:
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    response = client.translate(content=[text], to=[target_language])
    translated = response[0].translations[0].text if response and response[0].translations else text
    return {"translated_text": translated, "target_language": target_language}
