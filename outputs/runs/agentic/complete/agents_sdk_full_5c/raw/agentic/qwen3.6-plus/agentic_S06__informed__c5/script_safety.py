"""Check narration scripts for unsafe content using Azure AI Content Safety."""

import os
import base64
from typing import Optional
from urllib.parse import urljoin

import requests


AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def get_content_safety_endpoint() -> str:
    """Retrieve the Azure AI Content Safety endpoint from environment."""
    endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    if not endpoint:
        raise ValueError(
            f"{AZURE_CONTENT_SAFETY_ENDPOINT_ENV} environment variable is required"
        )
    return endpoint.rstrip("/")


def get_content_safety_key() -> str:
    """Retrieve the Azure AI Content Safety key from environment."""
    key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)
    if not key:
        raise ValueError(
            f"{AZURE_CONTENT_SAFETY_KEY_ENV} environment variable is required"
        )
    return key


def build_content_safety_url(endpoint: str) -> str:
    """Build the Azure AI Content Safety text analysis URL."""
    return urljoin(
        endpoint + "/",
        f"contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}",
    )


def check_script_safety(
    text: str,
    *,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    categories: Optional[list[str]] = None,
) -> dict:
    """Check narration script for unsafe content using Azure AI Content Safety.

    Sends the script text to the Azure AI Content Safety API
    (azure-ai-contentsafety endpoint) and evaluates it across content harm
    categories such as hate, self-harm, sexual, and violence.

    Args:
        text: The narration script text to evaluate.
        endpoint: Azure Content Safety service endpoint URL.
        api_key: Azure Content Safety access key.
        categories: Optional list of category names to evaluate.
            Defaults to ["Hate", "SelfHarm", "Sexual", "Violence"].

    Returns:
        Dict with analysis results including per-category severity scores
        and an overall safety verdict.
    """
    if endpoint is None:
        endpoint = get_content_safety_endpoint()
    if api_key is None:
        api_key = get_content_safety_key()

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    url = build_content_safety_url(endpoint)

    payload = {
        "text": text,
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()
    return _normalize_safety_response(result)


def _normalize_safety_response(raw_response: dict) -> dict:
    """Normalize Azure Content Safety response to a consistent schema."""
    category_scores = {}
    max_severity = 0
    unsafe_categories = []

    for analysis in raw_response.get("categoriesAnalysis", []):
        category = analysis.get("category", "Unknown")
        severity = analysis.get("severity", 0)
        category_scores[category] = severity
        if severity > max_severity:
            max_severity = severity
        if severity >= 4:
            unsafe_categories.append(category)

    is_safe = len(unsafe_categories) == 0

    return {
        "is_safe": is_safe,
        "max_severity": max_severity,
        "category_scores": category_scores,
        "unsafe_categories": unsafe_categories,
        "raw_response": raw_response,
    }
