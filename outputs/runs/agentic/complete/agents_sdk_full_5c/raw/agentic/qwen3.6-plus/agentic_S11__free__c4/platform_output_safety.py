"""Check platform model output for unsafe content.

Provider: Azure AI Content Safety (https://learn.microsoft.com/azure/ai-services/content-safety/)
SDK: azure-ai-contentsafety >= 1.0.0 with ContentSafetyClient.
Uses Azure AI Content Safety to analyze text output from the model platform
for hate, self-harm, sexual, and violence categories.
"""

from __future__ import annotations

import os
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
)
from azure.core.credentials import AzureKeyCredential

from model_models import SafetyResult


# Azure AI Content Safety provider-specific configuration
_AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
_AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
_AZURE_CONTENT_SAFETY_API_VERSION = os.environ.get(
    "AZURE_CONTENT_SAFETY_API_VERSION", "2024-09-01"
)


def resolve_content_safety_endpoint() -> str:
    """Return the Azure AI Content Safety endpoint from environment."""
    endpoint = os.environ.get(_AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    if not endpoint:
        raise RuntimeError(
            f"Missing provider environment variable: {_AZURE_CONTENT_SAFETY_ENDPOINT_ENV}. "
            f"Expected format: https://<resource-name>.cognitiveservices.azure.com/"
        )
    return endpoint.rstrip("/")


def resolve_content_safety_key() -> str:
    """Return the Azure AI Content Safety API key from environment."""
    key = os.environ.get(_AZURE_CONTENT_SAFETY_KEY_ENV)
    if not key:
        raise RuntimeError(
            f"Missing provider environment variable: {_AZURE_CONTENT_SAFETY_KEY_ENV}"
        )
    return key


def build_content_safety_client(
    *,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ContentSafetyClient:
    """Build a provider-specific Azure AI Content Safety client.

    Args:
        endpoint: Azure Content Safety endpoint. Resolved from env if not provided.
        api_key: Azure API key. Resolved from env if not provided.

    Returns:
        Configured ContentSafetyClient.
    """
    resolved_endpoint = endpoint or resolve_content_safety_endpoint()
    resolved_key = api_key or resolve_content_safety_key()

    credential = AzureKeyCredential(resolved_key)
    client = ContentSafetyClient(
        endpoint=resolved_endpoint,
        credential=credential,
    )
    return client


def check_platform_output_safety(
    *,
    text: str,
    client: Optional[ContentSafetyClient] = None,
    categories: Optional[list[TextCategory]] = None,
    halt_on_unsafe: bool = True,
) -> SafetyResult:
    """Check platform model output for unsafe content using Azure AI Content Safety.

    Analyzes text against Azure's four safety categories: Hate, SelfHarm,
    Sexual, and Violence. Each category returns a severity score (0-7).

    Args:
        text: The model output text to analyze.
        client: Pre-built ContentSafetyClient. Built automatically if not provided.
        categories: Specific TextCategory values to check. Defaults to all four.
        halt_on_unsafe: If True, raises RuntimeError when content is flagged as unsafe.

    Returns:
        SafetyResult with category severities and safety determination.

    Raises:
        RuntimeError: If halt_on_unsafe is True and content is deemed unsafe.
    """
    if client is None:
        client = build_content_safety_client()

    if categories is None:
        categories = [
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ]

    request = AnalyzeTextOptions(
        text=text,
        categories=categories,
    )

    response = client.analyze_text(request)

    result = SafetyResult.from_azure_safety(response)

    if halt_on_unsafe and not result.is_safe:
        raise RuntimeError(
            "Azure AI Content Safety flagged output as unsafe. "
            f"Categories: {result.categories}"
        )

    return result


def check_platform_output_with_blocklist(
    *,
    text: str,
    blocklist_names: list[str],
    client: Optional[ContentSafetyClient] = None,
) -> SafetyResult:
    """Check platform output against both Azure safety categories and custom blocklists.

    Blocklists allow custom keyword/pattern matching defined in the Azure
    Content Safety resource.

    Args:
        text: The model output text to analyze.
        blocklist_names: List of Azure Content Safety blocklist names to check against.
        client: Pre-built ContentSafetyClient. Built automatically if not provided.

    Returns:
        SafetyResult including blocklist match details.
    """
    if client is None:
        client = build_content_safety_client()

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
        blocklist_names=blocklist_names,
    )

    response = client.analyze_text(request)
    return SafetyResult.from_azure_safety(response)
