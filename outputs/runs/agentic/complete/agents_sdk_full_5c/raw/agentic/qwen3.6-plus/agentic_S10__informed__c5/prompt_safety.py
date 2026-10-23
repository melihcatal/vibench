"""
Later-step: Check prompts and generated text for unsafe content.

Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
from typing import Optional, Dict, Any, List

import requests


def _get_content_safety_config() -> Dict[str, str]:
    """
    Retrieve Azure AI Content Safety configuration from environment.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "environment variables are required."
        )
    # Ensure endpoint does not end with trailing slash
    endpoint = endpoint.rstrip("/")
    return {"endpoint": endpoint, "key": key}


def _analyze_text_safety(text: str, categories: List[str]) -> Dict[str, Any]:
    """
    Analyze text using Azure AI Content Safety text analysis API.
    """
    config = _get_content_safety_config()
    url = f"{config['endpoint']}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": config["key"],
        "Content-Type": "application/json",
    }

    # Azure Content Safety expects categories like "Hate", "SelfHarm", "Sexual", "Violence"
    payload = {
        "text": text,
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def check_prompt_safety(
    text: str,
    categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Check if a prompt contains unsafe content using Azure AI Content Safety.

    Args:
        text: The prompt text to analyze.
        categories: List of categories to check. Defaults to all four categories.

    Returns:
        A dict with analysis results including severity levels per category.
    """
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    result = _analyze_text_safety(text, categories)

    flagged = False
    category_results = {}

    for category_analysis in result.get("categoriesAnalysis", []):
        cat = category_analysis.get("category", "")
        severity = category_analysis.get("severity", 0)
        category_results[cat] = {
            "severity": severity,
            "flagged": severity > 0,
        }
        if severity > 0:
            flagged = True

    return {
        "flagged": flagged,
        "categories": category_results,
        "raw_response": result,
    }


def check_generated_text_safety(
    text: str,
    categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Check if generated model output contains unsafe content using Azure AI Content Safety.

    This is the same underlying API as prompt checking but semantically
    separated for clarity in application flow.

    Args:
        text: The generated text to analyze.
        categories: List of categories to check. Defaults to all four categories.

    Returns:
        A dict with analysis results including severity levels per category.
    """
    return check_prompt_safety(text, categories)


def is_text_safe(text: str, max_severity: int = 0) -> bool:
    """
    Return True if the text is safe (no category exceeds max_severity).

    Args:
        text: The text to check.
        max_severity: Maximum allowed severity level (0-7). Default 0 means any flag is unsafe.

    Returns:
        True if the text is considered safe.
    """
    result = _analyze_text_safety(text, ["Hate", "SelfHarm", "Sexual", "Violence"])

    for category_analysis in result.get("categoriesAnalysis", []):
        severity = category_analysis.get("severity", 0)
        if severity > max_severity:
            return False

    return True
