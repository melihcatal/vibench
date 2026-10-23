"""Translate platform model output for another locale.

Provider: Azure AI Translator (https://learn.microsoft.com/azure/ai-services/translator/)
SDK: azure-ai-translation-text >= 1.0.0 with DocumentTranslationClient / Translator client.
Uses the Azure AI Translator REST-based SDK for localized text translation.
"""

from __future__ import annotations

import os
from typing import Optional

from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential

from model_models import PlatformResponse


# Azure AI Translator provider-specific configuration
_AZURE_TRANSLATOR_ENDPOINT_ENV = "AZURE_TRANSLATOR_ENDPOINT"
_AZURE_TRANSLATOR_KEY_ENV = "AZURE_TRANSLATOR_KEY"
_AZURE_TRANSLATOR_REGION_ENV = "AZURE_TRANSLATOR_REGION"


def resolve_translator_endpoint() -> str:
    """Return the Azure AI Translator endpoint from environment."""
    endpoint = os.environ.get(_AZURE_TRANSLATOR_ENDPOINT_ENV)
    if not endpoint:
        raise RuntimeError(
            f"Missing provider environment variable: {_AZURE_TRANSLATOR_ENDPOINT_ENV}. "
            f"Expected format: https://api.cognitive.microsofttranslator.com/"
        )
    return endpoint.rstrip("/")


def resolve_translator_key() -> str:
    """Return the Azure AI Translator API key from environment."""
    key = os.environ.get(_AZURE_TRANSLATOR_KEY_ENV)
    if not key:
        raise RuntimeError(
            f"Missing provider environment variable: {_AZURE_TRANSLATOR_KEY_ENV}"
        )
    return key


def resolve_translator_region() -> str:
    """Return the Azure AI Translator region from environment."""
    region = os.environ.get(_AZURE_TRANSLATOR_REGION_ENV)
    if not region:
        raise RuntimeError(
            f"Missing provider environment variable: {_AZURE_TRANSLATOR_REGION_ENV}"
        )
    return region


def build_translator_client(
    *,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> TextTranslationClient:
    """Build a provider-specific Azure AI Text Translation client.

    Args:
        endpoint: Azure Translator endpoint. Resolved from env if not provided.
        api_key: Azure Translator API key. Resolved from env if not provided.

    Returns:
        Configured TextTranslationClient.
    """
    resolved_endpoint = endpoint or resolve_translator_endpoint()
    resolved_key = api_key or resolve_translator_key()
    resolved_region = resolve_translator_region()

    credential = AzureKeyCredential(resolved_key)
    client = TextTranslationClient(
        credential=credential,
        region=resolved_region,
        endpoint=resolved_endpoint,
    )
    return client


def localize_platform_output(
    *,
    text: str,
    target_language: str,
    client: Optional[TextTranslationClient] = None,
    source_language: Optional[str] = None,
) -> str:
    """Translate platform model output into another locale using Azure AI Translator.

    Uses the Azure Cognitive Services Translator API to translate text
    from the source language (auto-detected if not specified) to the target language.

    Args:
        text: The model output text to translate.
        target_language: BCP-47 target locale code (e.g., 'es', 'fr', 'ja', 'zh-Hans').
        client: Pre-built TextTranslationClient. Built automatically if not provided.
        source_language: Optional BCP-47 source locale. Auto-detected if None.

    Returns:
        Translated text string in the target locale.
    """
    if client is None:
        client = build_translator_client()

    input_item = InputTextItem(text=text)

    translate_kwargs: dict = {
        "body": [input_item],
        "to_language": [target_language],
    }

    if source_language:
        translate_kwargs["from_language"] = source_language

    response = client.translate(**translate_kwargs)

    if response and len(response) > 0:
        first_translation = response[0]
        if first_translation.translations:
            return first_translation.translations[0].text

    return text


def localize_platform_response(
    *,
    platform_response: PlatformResponse,
    target_language: str,
    client: Optional[TextTranslationClient] = None,
    source_language: Optional[str] = None,
) -> PlatformResponse:
    """Translate the content of a PlatformResponse into another locale.

    Args:
        platform_response: The original PlatformResponse from the model platform.
        target_language: BCP-47 target locale code.
        client: Pre-built TextTranslationClient. Built automatically if not provided.
        source_language: Optional BCP-47 source locale.

    Returns:
        New PlatformResponse with translated content and original metadata preserved.
    """
    translated_text = localize_platform_output(
        text=platform_response.content,
        target_language=target_language,
        client=client,
        source_language=source_language,
    )

    return PlatformResponse(
        content=translated_text,
        finish_reason=platform_response.finish_reason,
        model_id=platform_response.model_id,
        usage=platform_response.usage,
        system_fingerprint=platform_response.system_fingerprint,
        request_id=platform_response.request_id,
    )


def batch_localize_platform_outputs(
    *,
    texts: list[str],
    target_language: str,
    client: Optional[TextTranslationClient] = None,
    source_language: Optional[str] = None,
) -> list[str]:
    """Translate multiple platform outputs in a single Azure Translator request.

    Args:
        texts: List of model output strings to translate.
        target_language: BCP-47 target locale code.
        client: Pre-built TextTranslationClient. Built automatically if not provided.
        source_language: Optional BCP-47 source locale.

    Returns:
        List of translated strings in input order.
    """
    if client is None:
        client = build_translator_client()

    input_items = [InputTextItem(text=t) for t in texts]

    translate_kwargs: dict = {
        "body": input_items,
        "to_language": [target_language],
    }

    if source_language:
        translate_kwargs["from_language"] = source_language

    response = client.translate(**translate_kwargs)

    results = []
    for item in response:
        if item.translations:
            results.append(item.translations[0].text)
        else:
            results.append("")

    return results
