from __future__ import annotations

import os
from typing import Iterable

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY", "")
TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "")


def welcome_translate(text: str, target_locale: str, source_locale: str = "en") -> str:
    client = TextTranslationClient(
        endpoint="https://api.cognitive.microsofttranslator.com",
        credential=AzureKeyCredential(TRANSLATOR_KEY),
        region=TRANSLATOR_REGION,
    )
    result = client.translate(content=[text], to=[target_locale], from_parameter=source_locale)
    return result[0].translations[0].text
