"""
Check localized copy for unsafe content.

Provider: Azure AI Content Safety
SDK: requests (REST)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
from typing import Any, Dict, List, Optional

import requests


def check_unsafe_copy(
    text: str,
    categories: Optional[List[str]] = None,
    output_type: int = 0,
) -> Dict[str, Any]:
    """
    Check localized copy for unsafe content using Azure AI Content Safety.

    Args:
        text: The localized text to check.
        categories: Optional list of categories to check (e.g., ["Hate", "Sexual", "SelfHarm", "Violence"]).
        output_type: Response detail level (0=basic, 1=detailed).

    Returns:
        Dictionary with safety analysis results per category.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

    if not endpoint or not api_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "environment variables are required."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    categories_to_check = categories or ["Hate", "Sexual", "SelfHarm", "Violence"]
    payload = {
        "text": text,
        "output_type": output_type,
        "categories": categories_to_check,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return {
        "text": text,
        "safety_analysis": result,
        "categories_checked": categories_to_check,
        "has_issues": any(
            item.get("severity", 0) > 0
            for item in result.get("categoriesAnalysis", [])
        ),
    }


def check_localized_copy_batch(
    texts: List[str],
    categories: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Check a batch of localized strings for unsafe content.

    Args:
        texts: List of localized text strings to check.
        categories: Optional list of categories to check.

    Returns:
        List of analysis results per text.
    """
    results = []
    for text in texts:
        result = check_unsafe_copy(text, categories=categories)
        results.append(result)
    return results


def scan_translation_results(
    translations: Dict[str, str],
    target_lang: str,
) -> Dict[str, Dict[str, Any]]:
    """
    Scan all values in a translated dictionary for unsafe content.

    Args:
        translations: Dictionary of translated key-value pairs.
        target_lang: Target language code.

    Returns:
        Dictionary mapping keys to their safety analysis results.
    """
    flagged = {}
    for key, text in translations.items():
        result = check_unsafe_copy(text)
        if result["has_issues"]:
            flagged[key] = result
    return flagged


def is_copy_safe(text: str, threshold: int = 2) -> bool:
    """
    Quick check: is the text safe below the given severity threshold?

    Args:
        text: Text to check.
        threshold: Maximum allowed severity level (0-7).

    Returns:
        True if all categories are below the threshold.
    """
    result = check_unsafe_copy(text)
    for item in result.get("safety_analysis", {}).get("categoriesAnalysis", []):
        if item.get("severity", 0) >= threshold:
            return False
    return True


if __name__ == "__main__":
    sample = "This is a test of the content safety system."
    result = check_unsafe_copy(sample)
    print(result)
