"""
[LATER-STEP] Moderate profile text before account activation.

Provider: Azure AI Content Safety
- SDK: requests (REST)
- Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
from typing import Any, Dict, List, Optional

import requests


CONTENT_SAFETY_API_VERSION = "2024-09-01"

PROFILE_FIELDS_TO_MODERATE = [
    "display_name",
    "bio",
    "about_me",
    "status_message",
]


def _build_azure_content_safety_url(endpoint: str) -> str:
    """Build the Azure AI Content Safety text analysis URL."""
    endpoint = endpoint.rstrip("/")
    return f"{endpoint}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"


def _build_azure_headers(api_key: str) -> Dict[str, str]:
    """Build headers for Azure AI Content Safety API requests."""
    return {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }


def moderate_profile_text(
    profile_data: Dict[str, str],
    threshold: int = 4,
    categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Moderate user profile text fields using Azure AI Content Safety API.

    Analyzes each text field for Hate, SelfHarm, Sexual, and Violence categories.
    Uses the REST interface with AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY.

    Returns a moderation report per field and an overall approval flag.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").strip()
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "").strip()

    if not endpoint or not api_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    url = _build_azure_content_safety_url(endpoint)
    headers = _build_azure_headers(api_key)

    field_results: Dict[str, Any] = {}
    overall_safe = True

    for field_name in PROFILE_FIELDS_TO_MODERATE:
        text = profile_data.get(field_name, "").strip()
        if not text:
            field_results[field_name] = {"status": "skipped", "reason": "empty"}
            continue

        payload = {
            "text": text,
            "categories": categories,
            "outputType": "FourSeverityLevels",
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            analysis = response.json()

            category_scores = {}
            field_flagged = False

            for cat_result in analysis.get("categoriesAnalysis", []):
                cat_name = cat_result.get("category", "Unknown")
                severity = cat_result.get("severity", 0)
                category_scores[cat_name] = severity
                if severity >= threshold:
                    field_flagged = True

            if field_flagged:
                overall_safe = False
                field_results[field_name] = {
                    "status": "flagged",
                    "category_scores": category_scores,
                    "threshold": threshold,
                }
            else:
                field_results[field_name] = {
                    "status": "approved",
                    "category_scores": category_scores,
                }

        except requests.RequestException as exc:
            field_results[field_name] = {
                "status": "error",
                "error": str(exc),
            }
            overall_safe = False

    return {
        "approved": overall_safe,
        "field_results": field_results,
        "threshold": threshold,
    }


def moderate_single_text(text: str, threshold: int = 4) -> Dict[str, Any]:
    """Moderate a single text string using Azure AI Content Safety."""
    return moderate_profile_text({"input": text}, threshold=threshold)


if __name__ == "__main__":
    sample_profile = {
        "display_name": "John Doe",
        "bio": "Hello! I am a software developer.",
        "about_me": "",
        "status_message": "Available for collaboration",
    }
    result = moderate_profile_text(sample_profile)
    print(result)
