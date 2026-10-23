"""
secret_label_safety.py - Check secret labels and notes for unsafe text using Azure AI Content Safety.

Provider: Azure AI Content Safety
SDK: requests (REST interface)
Auth env vars: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
Service hostname: <endpoint>.cognitiveservices.azure.com
API version: 2024-02-15-preview
"""

import os
import logging
from typing import List, Dict, Any, Optional

import requests

from security_models import SecretLabelCheck

logger = logging.getLogger(__name__)

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT", ""
).rstrip("/")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"

# Default safety categories to check
_DEFAULT_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]

# Threshold above which content is considered unsafe (0-7 scale)
UNSAFE_THRESHOLD = 2


def _build_text_analysis_url() -> str:
    """Build the Azure AI Content Safety analyze text endpoint URL."""
    if not AZURE_CONTENT_SAFETY_ENDPOINT:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable is not set")
    return (
        f"{AZURE_CONTENT_SAFETY_ENDPOINT}"
        f"/contentsafety/text:analyze"
        f"?api-version={CONTENT_SAFETY_API_VERSION}"
    )


def analyze_text_safety(text: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Analyze text for unsafe content using Azure AI Content Safety REST API.

    Args:
        text: The text to analyze.
        categories: List of categories to check. Defaults to Hate, SelfHarm, Sexual, Violence.

    Returns:
        Dict with category scores and an overall safety assessment.

    Raises:
        requests.HTTPError: On API errors.
        ValueError: If required config is missing.
    """
    if not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is not set")

    if categories is None:
        categories = _DEFAULT_CATEGORIES

    url = _build_text_analysis_url()

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
    }

    body = {
        "text": text,
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    result = response.json()

    # Build per-category score map
    category_scores = {}
    for cat_result in result.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "Unknown")
        severity = cat_result.get("severity", 0)
        category_scores[cat_name] = severity

    # Determine overall safety
    max_severity = max(category_scores.values()) if category_scores else 0
    is_safe = max_severity < UNSAFE_THRESHOLD

    flagged = [cat for cat, sev in category_scores.items() if sev >= UNSAFE_THRESHOLD]

    return {
        "is_safe": is_safe,
        "category_scores": category_scores,
        "max_severity": max_severity,
        "flagged_categories": flagged,
    }


def check_secret_label_safety(
    secret_name: str,
    label: str = "",
    description: str = "",
) -> SecretLabelCheck:
    """
    Check a secret's label and description for unsafe content.

    Returns a SecretLabelCheck dataclass with safety assessment results.
    """
    combined_text = f"{label} {description}".strip()
    if not combined_text:
        return SecretLabelCheck(
            name=secret_name,
            label=label,
            description=description,
            is_safe=True,
            flagged_terms=[],
            confidence=1.0,
        )

    try:
        analysis = analyze_text_safety(combined_text)
    except Exception as exc:
        logger.error("Safety analysis failed for secret '%s': %s", secret_name, exc)
        return SecretLabelCheck(
            name=secret_name,
            label=label,
            description=description,
            is_safe=True,
            flagged_terms=["analysis_failed"],
            confidence=0.0,
        )

    max_severity = analysis.get("max_severity", 0)
    confidence = 1.0 if analysis["is_safe"] else max(0.1, 1.0 - (max_severity / 7.0))

    return SecretLabelCheck(
        name=secret_name,
        label=label,
        description=description,
        is_safe=analysis["is_safe"],
        flagged_terms=analysis.get("flagged_categories", []),
        confidence=round(confidence, 2),
    )


def batch_check_secret_labels(
    secrets: List[Dict[str, str]],
) -> List[SecretLabelCheck]:
    """
    Batch-check labels and descriptions for multiple secrets.

    Args:
        secrets: List of dicts with keys 'name', 'label', 'description'.

    Returns:
        List of SecretLabelCheck results.
    """
    results = []
    for secret in secrets:
        result = check_secret_label_safety(
            secret_name=secret.get("name", ""),
            label=secret.get("label", ""),
            description=secret.get("description", ""),
        )
        results.append(result)
    return results
