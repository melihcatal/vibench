"""
Check narration scripts for unsafe content using Azure AI Content Safety.

Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
from typing import Optional, Dict, Any, List

import requests

AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"

# Azure Content Safety API version
API_VERSION = "2024-02-15-preview"

# Content safety categories
CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]


def get_azure_content_safety_config(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, str]:
    """Get Azure Content Safety configuration from environment or params.

    Args:
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Returns:
        Dict with endpoint and api_key.
    """
    ep = endpoint or os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV)
    key = api_key or os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV)

    if not ep:
        raise ValueError(
            f"Azure Content Safety endpoint not set. "
            f"Set {AZURE_CONTENT_SAFETY_ENDPOINT_ENV}."
        )
    if not key:
        raise ValueError(
            f"Azure Content Safety key not set. "
            f"Set {AZURE_CONTENT_SAFETY_KEY_ENV}."
        )

    # Normalize endpoint URL
    ep = ep.rstrip("/")
    return {"endpoint": ep, "api_key": key}


def check_script_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    block_threshold: int = 4,
    categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Check narration script for unsafe content using Azure AI Content Safety.

    Args:
        text: Script text to analyze.
        endpoint: Azure Content Safety endpoint.
        api_key: Azure Content Safety API key.
        block_threshold: Severity threshold (0-8) for flagging content.
        categories: Categories to check. Defaults to all.

    Returns:
        Dict with safety analysis results.
    """
    config = get_azure_content_safety_config(endpoint, api_key)
    base_url = config["endpoint"]

    url = f"{base_url}/contentsafety/text:analyze?api-version={API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": config["api_key"],
        "Content-Type": "application/json",
    }

    check_categories = categories or CATEGORIES
    categories_payload = [{"category": cat} for cat in check_categories]

    payload = {
        "text": text,
        "categories": categories_payload,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    # Parse results
    category_scores = {}
    flagged = False
    flagged_categories = []

    for item in result.get("categoriesAnalysis", []):
        cat = item.get("category", "")
        severity = item.get("severity", 0)
        category_scores[cat] = severity
        if severity >= block_threshold:
            flagged = True
            flagged_categories.append(cat)

    return {
        "safe": not flagged,
        "flagged": flagged,
        "flagged_categories": flagged_categories,
        "category_scores": category_scores,
        "block_threshold": block_threshold,
        "blocklist_match": result.get("blocklistsMatch", []),
    }


def check_script_safety_batch(
    texts: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    block_threshold: int = 4,
) -> List[Dict[str, Any]]:
    """Batch check multiple scripts for unsafe content.

    Args:
        texts: List of script texts.
        endpoint: Azure Content Safety endpoint.
        api_key: Azure Content Safety API key.
        block_threshold: Severity threshold for flagging.

    Returns:
        List of safety analysis results.
    """
    results = []
    for text in texts:
        result = check_script_safety(
            text=text,
            endpoint=endpoint,
            api_key=api_key,
            block_threshold=block_threshold,
        )
        result["text"] = text
        results.append(result)
    return results


def get_safety_recommendation(
    safety_result: Dict[str, Any],
) -> str:
    """Get a human-readable recommendation from safety analysis.

    Args:
        safety_result: Result from check_script_safety.

    Returns:
        Recommendation string.
    """
    if safety_result.get("safe"):
        return "PASS: Content is safe for synthesis."

    flagged = safety_result.get("flagged_categories", [])
    scores = safety_result.get("category_scores", {})

    details = []
    for cat in flagged:
        severity = scores.get(cat, 0)
        details.append(f"{cat} (severity: {severity})")

    return f"BLOCK: Unsafe content detected in categories: {', '.join(details)}"
