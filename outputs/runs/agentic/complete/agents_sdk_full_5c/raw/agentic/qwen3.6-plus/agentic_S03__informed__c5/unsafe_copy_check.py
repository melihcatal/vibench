"""
unsafe_copy_check.py - Check localized copy for unsafe content using Azure AI Content Safety.

Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY environment variables
Endpoint: https://{resource-name}.cognitiveservices.azure.com
"""

import os
from typing import Dict, List, Optional

import requests


AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def _build_text_analysis_payload(texts: List[str]) -> dict:
    """Build the request payload for Azure AI Content Safety text analysis."""
    return {
        "text": "\n".join(texts),
        "outputType": "FourSeverityLevels",
    }


def _map_severity_level(level: str) -> int:
    """Map Azure severity level names to numeric values."""
    mapping = {
        "Safe": 0,
        "Low": 1,
        "Medium": 2,
        "High": 3,
    }
    return mapping.get(level, 0)


def check_unsafe_copy(
    texts: List[str],
    categories: Optional[List[str]] = None,
    threshold: int = 2,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict:
    """
    Check localized copy for unsafe or harmful content using Azure AI Content Safety.

    Analyzes text for hate speech, sexual content, violence, and self-harm categories.

    Args:
        texts: List of localized text strings to analyze.
        categories: Specific content categories to check. Defaults to all:
            ['Hate', 'SelfHarm', 'Sexual', 'Violence'].
        threshold: Severity threshold (0-3). Texts exceeding this are flagged.
            0=Safe, 1=Low, 2=Medium, 3=High. Defaults to 2 (flags Medium and High).
        endpoint: Azure Content Safety endpoint URL. If None, reads from
            AZURE_CONTENT_SAFETY_ENDPOINT env variable.
        api_key: Azure Content Safety API key. If None, reads from
            AZURE_CONTENT_SAFETY_KEY env variable.

    Returns:
        Dict with analysis results:
        {
            "flagged_texts": [{"index": int, "text": str, "categories": dict}],
            "safe_texts": [{"index": int, "text": str}],
            "overall_status": "safe" | "flagged",
            "total_analyzed": int,
            "total_flagged": int,
        }

    Raises:
        ValueError: If endpoint or api_key is not provided.
        requests.exceptions.RequestException: If the Azure API request fails.
    """
    az_endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    az_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

    if not az_endpoint:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable or endpoint parameter "
            "is required for Azure AI Content Safety."
        )
    if not az_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY environment variable or api_key parameter "
            "is required for Azure AI Content Safety."
        )

    if not texts:
        return {
            "flagged_texts": [],
            "safe_texts": [],
            "overall_status": "safe",
            "total_analyzed": 0,
            "total_flagged": 0,
        }

    # Clean up endpoint URL
    endpoint = az_endpoint.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": az_key,
        "Content-Type": "application/json",
    }

    payload = _build_text_analysis_payload(texts)

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    categories_to_check = categories or ["Hate", "SelfHarm", "Sexual", "Violence"]

    flagged_texts = []
    safe_texts = []

    for i, text in enumerate(texts):
        text_categories = {}
        text_severity_exceeded = False

        for category in categories_to_check:
            severity_key = f"{category}Result"
            category_result = result.get(severity_key, {})
            severity_level = category_result.get("severity", "Safe")
            severity_value = _map_severity_level(severity_level)
            text_categories[category] = {
                "severity": severity_level,
                "severity_value": severity_value,
            }
            if severity_value >= threshold:
                text_severity_exceeded = True

        if text_severity_exceeded:
            flagged_texts.append({
                "index": i,
                "text": text,
                "categories": text_categories,
            })
        else:
            safe_texts.append({
                "index": i,
                "text": text,
                "categories": text_categories,
            })

    return {
        "flagged_texts": flagged_texts,
        "safe_texts": safe_texts,
        "overall_status": "flagged" if flagged_texts else "safe",
        "total_analyzed": len(texts),
        "total_flagged": len(flagged_texts),
    }
