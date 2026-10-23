"""Check localized copy for unsafe content using Azure AI Content Safety.

Analyzes translated text for hate speech, sexual content, violence,
and self-harm indicators using Azure's content moderation API.
"""

import os
from typing import Any

import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT", "https://<your-resource>.cognitiveservices.azure.com/"
)
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"

CATEGORY_LABELS = {
    "Hate": "hate_speech",
    "SelfHarm": "self_harm",
    "Sexual": "sexual_content",
    "Violence": "violence",
}


def check_unsafe_content(
    text: str,
    categories: list[str] | None = None,
    endpoint: str | None = None,
) -> dict[str, Any]:
    """Analyze localized copy for unsafe content using Azure AI Content Safety.

    Args:
        text: The translated/localized text to check.
        categories: Optional list of categories to check (Hate, SelfHarm, Sexual, Violence).
        endpoint: Optional Azure endpoint override (defaults to AZURE_CONTENT_SAFETY_ENDPOINT).

    Returns:
        Dictionary with safety scores, flagged categories, and an overall safety verdict.
    """
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not api_key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required for Azure AI Content Safety")

    base_endpoint = endpoint or AZURE_CONTENT_SAFETY_ENDPOINT
    if not base_endpoint.endswith("/"):
        base_endpoint += "/"

    url = f"{base_endpoint}contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    # Default to all categories if none specified
    text_categories = categories or ["Hate", "SelfHarm", "Sexual", "Violence"]

    payload: dict[str, Any] = {
        "text": text,
        "categories": text_categories,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()

    return _parse_safety_response(result, text)


def _parse_safety_response(result: dict[str, Any], original_text: str) -> dict[str, Any]:
    """Parse Azure Content Safety response into a standardized format.

    Args:
        result: Raw response from Azure Content Safety API.
        original_text: The text that was analyzed.

    Returns:
        Standardized safety check result.
    """
    flagged_categories: list[str] = []
    category_scores: dict[str, int] = {}
    max_severity = 0

    for analysis in result.get("categoriesAnalysis", []):
        category = analysis.get("category", "")
        severity = analysis.get("severity", 0)
        friendly_name = CATEGORY_LABELS.get(category, category.lower())
        category_scores[friendly_name] = severity

        if severity >= 4:
            flagged_categories.append(friendly_name)

        if severity > max_severity:
            max_severity = severity

    # Check for blocklist matches
    blocklist_matches = result.get("blocklistsMatch", [])
    has_blocklist_match = len(blocklist_matches) > 0

    if has_blocklist_match:
        for match in blocklist_matches:
            flagged_categories.append(f"blocklist:{match.get('blocklistName', 'unknown')}")

    is_unsafe = len(flagged_categories) > 0 or has_blocklist_match

    return {
        "text_length": len(original_text),
        "is_unsafe": is_unsafe,
        "flagged_categories": flagged_categories,
        "category_scores": category_scores,
        "max_severity": max_severity,
        "blocklist_matches": blocklist_matches,
        "provider": "azure_ai_content_safety",
    }


def batch_unsafe_copy_check(
    texts: list[str],
    categories: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Check multiple localized texts for unsafe content using Azure AI Content Safety.

    Args:
        texts: List of translated/localized texts to check.
        categories: Optional list of categories to check.

    Returns:
        List of safety check results corresponding to each input text.
    """
    results: list[dict[str, Any]] = []
    for text in texts:
        result = check_unsafe_content(text, categories=categories)
        results.append(result)
    return results
