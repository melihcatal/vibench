from __future__ import annotations

from typing import Any, Dict

from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient

from identity_models import TranslationRequest, normalize_locale


def welcome_translate(request: TranslationRequest | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(request, dict):
        request = TranslationRequest(**request)
    endpoint = __import__("os").environ.get("AZURE_TRANSLATOR_ENDPOINT", "")
    key = __import__("os").environ.get("AZURE_TRANSLATOR_KEY", "")
    region = __import__("os").environ.get("AZURE_TRANSLATOR_REGION", "")
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key), region=region)
    response = client.translate(content=[request.text], to=[normalize_locale(request.target_locale)], from_parameter=request.source_locale)
    return {"translations": [item.text for item in response[0].translations], "target_locale": normalize_locale(request.target_locale)}
