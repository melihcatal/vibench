"""Check narration scripts for unsafe content using Azure AI Content Safety."""

import os
from typing import Dict, List, Optional

import requests


def check_script_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    categories: Optional[List[str]] = None,
) -> Dict:
    """Analyze a narration script for unsafe content using Azure AI Content Safety.

    Azure AI Content Safety evaluates text for hate, self-harm, sexual, and violence categories.
    Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars
    if not explicitly provided.

    Args:
        text: The narration script text to analyze.
        endpoint: Azure Content Safety endpoint URL
            (e.g. "https://<resource>.cognitiveservices.azure.com/").
        api_key: Azure Content Safety API key.
        categories: Optional list of category keys to check:
            "Hate", "SelfHarm", "Sexual", "Violence".

    Returns:
        Dict with 'is_safe' (bool), 'categories' (dict of scores),
        and 'blocklists_match' info from Azure Content Safety.
    """
    endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "Azure Content Safety credentials required. "
            "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY."
        )

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    categories_to_check = categories or ["Hate", "SelfHarm", "Sexual", "Violence"]
    body = {
        "text": text,
        "categories": categories_to_check,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()

    is_safe = True
    category_scores = {}
    for category_result in result.get("categoriesAnalysis", []):
        cat_name = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        category_scores[cat_name] = severity
        if severity > 0:
            is_safe = False

    blocklists = result.get("blocklistsMatch", [])

    return {
        "is_safe": is_safe,
        "categories": category_scores,
        "blocklists_match": blocklists,
        "provider": "azure_ai_content_safety",
    }


def get_safety_summary(
    safety_result: Dict,
    threshold: int = 2,
) -> Dict[str, str]:
    """Generate a human-readable safety summary from Azure Content Safety results.

    Args:
        safety_result: The result dict from check_script_safety.
        threshold: Severity level threshold (0-4). Scores >= threshold flag as unsafe.

    Returns:
        Summary dict with 'status', 'flags', and 'details'.
    """
    flags = []
    details = {}

    for cat, severity in safety_result.get("categories", {}).items():
        details[cat] = severity
        if severity >= threshold:
            flags.append(cat)

    status = "UNSAFE" if flags else "SAFE"

    return {
        "status": status,
        "flags": flags,
        "details": details,
    }


def batch_check_safety(
    texts: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> List[Dict]:
    """Batch-check multiple narration scripts with Azure AI Content Safety.

    Args:
        texts: List of script strings to analyze.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Returns:
        List of safety result dicts, one per input text.
    """
    results = []
    for text in texts:
        result = check_script_safety(
            text=text, endpoint=endpoint, api_key=api_key
        )
        results.append(result)
    return results
