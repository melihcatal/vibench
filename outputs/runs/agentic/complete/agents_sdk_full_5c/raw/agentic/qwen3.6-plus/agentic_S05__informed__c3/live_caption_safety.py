"""
Check live transcript text for unsafe content using Azure AI Content Safety.

Analyzes streaming transcript text for categories including hate, self-harm,
sexual, and violence content using Azure AI Content Safety service.

Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from __future__ import annotations

import os
from typing import AsyncGenerator, Optional

import requests

# Azure Content Safety provider constants
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"
AZURE_CONTENT_SAFETY_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]
AZURE_SEVERITY_LEVELS = {
    0: "Safe",
    2: "Low",
    4: "Medium",
    6: "High",
}


def _get_azure_safety_config() -> tuple[str, str]:
    """
    Get Azure Content Safety endpoint and key from environment.

    Returns:
        Tuple of (endpoint, key).

    Raises:
        EnvironmentError: If required environment variables are not set.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "environment variables must be set."
        )

    return endpoint.rstrip("/"), key


def _build_azure_safety_url(endpoint: str) -> str:
    """
    Build the Azure Content Safety analyze text URL.

    Args:
        endpoint: Azure Content Safety service endpoint.

    Returns:
        Full API URL for text analysis.
    """
    return (
        f"{endpoint}/contentsafety/text:analyze"
        f"?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    )


def check_text_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """
    Check a single text for unsafe content using Azure AI Content Safety.

    Args:
        text: Text content to analyze.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Returns:
        Dict with safety analysis results including per-category severities.
    """
    if not endpoint or not api_key:
        endpoint, api_key = _get_azure_safety_config()

    url = _build_azure_safety_url(endpoint)

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    category_scores = {}
    overall_severity = 0

    for category_result in result.get("categoriesAnalysis", []):
        cat_name = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        category_scores[cat_name] = severity
        overall_severity = max(overall_severity, severity)

    return {
        "text_preview": text[:100],
        "is_safe": overall_severity <= 2,
        "overall_severity": overall_severity,
        "overall_level": AZURE_SEVERITY_LEVELS.get(overall_severity, "Unknown"),
        "category_scores": category_scores,
        "categories_flagged": {
            cat: sev for cat, sev in category_scores.items() if sev >= 4
        },
    }


async def check_live_caption_safety(
    transcript_stream: AsyncGenerator[str, None],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    severity_threshold: int = 4,
) -> AsyncGenerator[dict, None]:
    """
    Check live transcript text for unsafe content using Azure AI Content Safety.

    Analyzes each incoming transcript text chunk against Azure's content safety
    moderation categories (Hate, Self-Harm, Sexual, Violence) and yields
    safety analysis results.

    Args:
        transcript_stream: Async generator yielding transcript text strings.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.
        severity_threshold: Minimum severity level to flag as unsafe (0-6).

    Yields:
        Dict with keys:
            - 'text_preview': First 100 chars of analyzed text
            - 'is_safe': Boolean indicating if text passed safety check
            - 'overall_severity': Maximum severity across all categories
            - 'overall_level': Human-readable severity level
            - 'category_scores': Per-category severity scores
            - 'categories_flagged': Categories exceeding the threshold
            - 'flagged': Whether this chunk should be flagged
    """
    if not endpoint or not api_key:
        endpoint, api_key = _get_azure_safety_config()

    url = _build_azure_safety_url(endpoint)

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    async for text in transcript_stream:
        if not text.strip():
            continue

        try:
            payload = {
                "text": text,
                "outputType": "FourSeverityLevels",
            }

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            result = response.json()

            category_scores = {}
            overall_severity = 0

            for category_result in result.get("categoriesAnalysis", []):
                cat_name = category_result.get("category", "")
                severity = category_result.get("severity", 0)
                category_scores[cat_name] = severity
                overall_severity = max(overall_severity, severity)

            flagged_categories = {
                cat: sev
                for cat, sev in category_scores.items()
                if sev >= severity_threshold
            }

            yield {
                "text_preview": text[:100],
                "is_safe": overall_severity < severity_threshold,
                "overall_severity": overall_severity,
                "overall_level": AZURE_SEVERITY_LEVELS.get(
                    overall_severity, "Unknown"
                ),
                "category_scores": category_scores,
                "categories_flagged": flagged_categories,
                "flagged": len(flagged_categories) > 0,
            }

        except requests.RequestException as e:
            yield {
                "text_preview": text[:100],
                "is_safe": False,
                "overall_severity": -1,
                "overall_level": "Error",
                "category_scores": {},
                "categories_flagged": {},
                "flagged": True,
                "error": str(e),
            }
