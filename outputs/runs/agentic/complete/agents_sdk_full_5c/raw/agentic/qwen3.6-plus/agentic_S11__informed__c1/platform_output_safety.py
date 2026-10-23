"""Check platform model output for unsafe content using Azure AI Content Safety.

Uses Azure AI Content Safety service with AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class SafetyAssessment:
    """Result of Azure AI Content Safety text analysis."""

    text: str
    is_safe: bool
    severity: str
    categories: dict[str, int]
    flagged_categories: list[str]
    raw_response: Optional[dict] = None


_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
_CONTENT_SAFETY_API_VERSION = "2024-09-01"


def _get_endpoint() -> str:
    endpoint = os.environ.get(_CONTENT_SAFETY_ENDPOINT_ENV, "")
    if not endpoint:
        raise ValueError(f"{_CONTENT_SAFETY_ENDPOINT_ENV} environment variable is not set")
    return endpoint.rstrip("/")


def _get_api_key() -> str:
    key = os.environ.get(_CONTENT_SAFETY_KEY_ENV, "")
    if not key:
        raise ValueError(f"{_CONTENT_SAFETY_KEY_ENV} environment variable is not set")
    return key


def _map_severity(score: int) -> str:
    """Map Azure AI Content Safety severity score to a human-readable level."""
    if score <= 1:
        return "safe"
    elif score <= 3:
        return "low"
    elif score <= 5:
        return "medium"
    else:
        return "high"


_CATEGORY_MAP = {
    "Hate": "hate",
    "SelfHarm": "self_harm",
    "Sexual": "sexual",
    "Violence": "violence",
}

_SEVERITY_THRESHOLD = 4


def check_platform_output_safety(
    text: str,
    threshold: int = _SEVERITY_THRESHOLD,
) -> SafetyAssessment:
    """Analyze text for unsafe content using Azure AI Content Safety API.

    Sends the text to the Azure AI Content Safety Analyze Text endpoint and
    evaluates the response against the severity threshold.

    Args:
        text: The text to evaluate for unsafe content.
        threshold: Severity score threshold (0-7). Content above this is flagged.

    Returns:
        SafetyAssessment with safety verdict, category scores, and flagged items.
    """
    endpoint = _get_endpoint()
    api_key = _get_api_key()
    api_version = _CONTENT_SAFETY_API_VERSION

    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    categories: dict[str, int] = {}
    flagged: list[str] = []
    max_severity = 0

    for category_result in result.get("categoriesAnalysis", []):
        category_name = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        friendly_name = _CATEGORY_MAP.get(category_name, category_name.lower())
        categories[friendly_name] = severity
        if severity > max_severity:
            max_severity = severity
        if severity >= threshold:
            flagged.append(friendly_name)

    is_safe = max_severity < threshold
    severity_label = _map_severity(max_severity)

    return SafetyAssessment(
        text=text,
        is_safe=is_safe,
        severity=severity_label,
        categories=categories,
        flagged_categories=flagged,
        raw_response=result,
    )


if __name__ == "__main__":
    sample = "This is a completely harmless sentence about sunshine and rainbows."
    result = check_platform_output_safety(sample)
    print(f"Safe: {result.is_safe}")
    print(f"Severity: {result.severity}")
    print(f"Categories: {result.categories}")
    print(f"Flagged: {result.flagged_categories}")
