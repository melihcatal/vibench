"""Check narration scripts for unsafe content using Azure AI Content Safety."""

import os
import requests
from typing import Optional, Dict, Any, List


CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"
AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"


def check_script_safety(
    text: str,
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Analyze narration script for unsafe content using Azure AI Content Safety.

    Args:
        text: The narration script text to analyze.
        categories: Optional list of categories to check.
            Defaults to ['Hate', 'SelfHarm', 'Sexual', 'Violence'].
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Returns:
        Dict with 'safe' (bool), 'categories' breakdown, and 'reasons' list.

    Raises:
        ValueError: If endpoint or key is missing.
        requests.HTTPError: If the API call fails.
    """
    if endpoint is None:
        endpoint = os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    if api_key is None:
        api_key = os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)

    if not endpoint:
        raise ValueError(
            f"{AZURE_CONTENT_SAFETY_ENDPOINT_ENV} environment variable is required."
        )
    if not api_key:
        raise ValueError(
            f"{AZURE_CONTENT_SAFETY_KEY_ENV} environment variable is required."
        )

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"

    default_categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    check_categories = categories or default_categories

    payload = {
        "text": text,
        "categories": check_categories,
        "outputType": "EightSeverityLevels",
    }

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    return _parse_safety_response(data)


def _parse_safety_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse Azure Content Safety API response into a standardized dict."""
    category_results = data.get("categoriesAnalysis", [])
    reasons = []
    is_safe = True

    severity_threshold = 4

    for cat_result in category_results:
        category_name = cat_result.get("category", "Unknown")
        severity = cat_result.get("severity", 0)

        if severity >= severity_threshold:
            is_safe = False
            reasons.append(
                f"{category_name} detected with severity {severity}/7"
            )

    result = {
        "safe": is_safe,
        "categories": {
            c.get("category", "Unknown"): c.get("severity", 0)
            for c in category_results
        },
        "reasons": reasons,
        "blocklists_match": data.get("blocklistsMatch", []),
    }

    return result


def check_script_safety_batch(
    texts: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Check multiple scripts for safety in parallel using Azure Content Safety.

    Args:
        texts: List of narration scripts to analyze.
        endpoint: Azure Content Safety endpoint.
        api_key: Azure Content Safety API key.

    Returns:
        List of safety analysis results, one per input text.
    """
    results = []
    for text in texts:
        result = check_script_safety(text, endpoint=endpoint, api_key=api_key)
        results.append(result)
    return results


def is_script_safe(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> bool:
    """Quick check: is the script safe for TTS synthesis?

    Args:
        text: The narration script text.
        endpoint: Azure Content Safety endpoint.
        api_key: Azure Content Safety API key.

    Returns:
        True if the script is safe, False otherwise.
    """
    result = check_script_safety(text, endpoint=endpoint, api_key=api_key)
    return result["safe"]


if __name__ == "__main__":
    result = check_script_safety("This is a safe narration script for testing.")
    print(f"Safe: {result['safe']}")
    print(f"Categories: {result['categories']}")
