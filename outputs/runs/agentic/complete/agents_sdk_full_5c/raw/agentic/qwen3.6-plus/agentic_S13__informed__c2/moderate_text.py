"""
moderate_text.py - Scores user text for unsafe or policy-violating content.

Provider: Azure AI Content Safety
  - SDK: azure-ai-contentsafety
  - Env: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
  - Endpoint: .cognitiveservices.azure.com
  - Categories: Hate, SelfHarm, Sexual, Violence
"""

from __future__ import annotations

from typing import Optional, Dict, Any

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from safety_client import create_content_safety_client
from safety_models import (
    ModerationRequest,
    ModerationResponse,
    normalize_azure_response,
    AZURE_CATEGORIES,
)

CATEGORY_MAP = {
    "Hate": TextCategory.HATE,
    "SelfHarm": TextCategory.SELF_HARM,
    "Sexual": TextCategory.SEXUAL,
    "Violence": TextCategory.VIOLENCE,
}


def moderate_text(
    text: str,
    categories: Optional[list[str]] = None,
    client: Optional[ContentSafetyClient] = None,
) -> ModerationResponse:
    """
    Analyze a single text input for unsafe content using Azure AI Content Safety.

    Args:
        text: The user-provided text to moderate.
        categories: Optional list of categories to analyze.
                    Defaults to all four Azure categories.
        client: Optional pre-configured ContentSafetyClient.

    Returns:
        ModerationResponse with per-category severity scores and overall safety flag.

    Raises:
        ValueError: If text is empty or credentials are missing.
    """
    if not text or not text.strip():
        raise ValueError("Input text must not be empty.")

    if client is None:
        client = create_content_safety_client()

    if categories is None:
        categories = AZURE_CATEGORIES

    text_categories = [CATEGORY_MAP[c] for c in categories if c in CATEGORY_MAP]

    options = AnalyzeTextOptions(
        text=text,
        categories=text_categories,
        output_type=0,  # Four severity levels
    )

    azure_response = client.analyze_text(options)

    return normalize_azure_response(text=text, azure_response=azure_response)


def moderate_text_with_blocklist(
    text: str,
    blocklist_name: str,
    categories: Optional[list[str]] = None,
    client: Optional[ContentSafetyClient] = None,
) -> ModerationResponse:
    """
    Analyze text for unsafe content and check against a custom blocklist.

    Args:
        text: The user-provided text to moderate.
        blocklist_name: Name of the Azure Content Safety custom blocklist.
        categories: Optional list of categories to analyze.
        client: Optional pre-configured ContentSafetyClient.

    Returns:
        ModerationResponse including blocklist match information.
    """
    if client is None:
        client = create_content_safety_client()

    if categories is None:
        categories = AZURE_CATEGORIES

    text_categories = [CATEGORY_MAP[c] for c in categories if c in CATEGORY_MAP]

    options = AnalyzeTextOptions(
        text=text,
        categories=text_categories,
        output_type=0,
        blocklist_names=[blocklist_name],
        halt_on_blocklist_match=False,
    )

    azure_response = client.analyze_text(options)

    blocklist_match = False
    if hasattr(azure_response, "blocklists_match") and azure_response.blocklists_match:
        blocklist_match = True
        matched_name = blocklist_name
    else:
        matched_name = None

    return normalize_azure_response(
        text=text,
        azure_response=azure_response,
        blocklist_match=blocklist_match,
        blocklist_name=matched_name,
    )


def get_severity_label(severity: int) -> str:
    """Convert an Azure severity integer to a human-readable label."""
    labels = {0: "safe", 2: "low", 4: "medium", 6: "high"}
    return labels.get(severity, "unknown")
