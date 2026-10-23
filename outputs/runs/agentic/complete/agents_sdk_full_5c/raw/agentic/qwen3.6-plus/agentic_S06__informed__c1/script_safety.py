"""
[LATER-STEP] script_safety.py
Check narration scripts for unsafe content using Azure AI Content Safety API.
"""
from typing import Optional, Dict, Any, List
import os
import requests
from speech_models import TTSRequest


AZURE_CONTENT_SAFETY_VERSION = "2024-02-15-preview"


class SafetyCheckError(Exception):
    """Raised when safety check fails."""
    pass


def build_azure_safety_endpoint() -> str:
    """Build the Azure AI Content Safety API endpoint from environment variables."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    if not endpoint:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is not set."
        )
    endpoint = endpoint.rstrip("/")
    return f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_VERSION}"


def get_azure_safety_key() -> str:
    """Get the Azure AI Content Safety API key from environment variables."""
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    if not key:
        raise EnvironmentError(
            "AZURE_CONTENT_SAFETY_KEY environment variable is not set."
        )
    return key


def check_script_safety(
    text: str,
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check narration script text for unsafe content using Azure AI Content Safety.

    Args:
        text: The text to analyze for safety.
        categories: Optional list of categories to check
            (e.g., ["Hate", "SelfHarm", "Sexual", "Violence"]).
        endpoint: Optional Azure Content Safety endpoint URL.
        api_key: Optional Azure Content Safety API key.

    Returns:
        Dictionary with analysis results including categories and severities.
    """
    if endpoint is None:
        endpoint = build_azure_safety_endpoint()
    if api_key is None:
        api_key = get_azure_safety_key()

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload: Dict[str, Any] = {"text": text}
    if categories:
        payload["categories"] = categories

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        raise SafetyCheckError(f"Azure Content Safety check failed: {e}") from e


def is_script_safe(
    text: str,
    max_severity: int = 2,
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> bool:
    """
    Determine if a script passes safety checks based on Azure AI Content Safety results.

    Args:
        text: The text to analyze.
        max_severity: Maximum allowed severity level (0-7). Returns False if any category exceeds this.
        categories: Optional list of categories to check.
        endpoint: Optional Azure Content Safety endpoint URL.
        api_key: Optional Azure Content Safety API key.

    Returns:
        True if the script is safe (all categories at or below max_severity), False otherwise.
    """
    result = check_script_safety(
        text=text,
        categories=categories,
        endpoint=endpoint,
        api_key=api_key,
    )

    categories_result = result.get("categoriesAnalysis", [])
    for cat_analysis in categories_result:
        severity = cat_analysis.get("severity", 0)
        if severity > max_severity:
            return False
    return True


def get_safety_summary(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get a human-readable safety summary for a script.

    Args:
        text: The text to analyze.
        endpoint: Optional Azure Content Safety endpoint URL.
        api_key: Optional Azure Content Safety API key.

    Returns:
        Summary dictionary with overall safety status and per-category details.
    """
    result = check_script_safety(
        text=text,
        endpoint=endpoint,
        api_key=api_key,
    )

    categories_result = result.get("categoriesAnalysis", [])
    category_details = {}
    overall_safe = True

    for cat_analysis in categories_result:
        category = cat_analysis.get("category", "Unknown")
        severity = cat_analysis.get("severity", 0)
        is_safe = severity <= 2
        category_details[category] = {
            "severity": severity,
            "safe": is_safe,
        }
        if not is_safe:
            overall_safe = False

    return {
        "overall_safe": overall_safe,
        "categories": category_details,
        "text_length": len(text),
        "provider": "azure_ai_content_safety",
    }


def check_tts_request_safety(
    request: TTSRequest,
    max_severity: int = 2,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check the text in a TTSRequest for unsafe content.

    Args:
        request: The TTSRequest to check.
        max_severity: Maximum allowed severity level.
        endpoint: Optional Azure Content Safety endpoint URL.
        api_key: Optional Azure Content Safety API key.

    Returns:
        Safety check result dictionary.
    """
    return get_safety_summary(
        text=request.text,
        endpoint=endpoint,
        api_key=api_key,
    )


if __name__ == "__main__":
    sample = "This is a safe narration script for a product demo."
    summary = get_safety_summary(sample)
    print(f"Safety summary: {summary}")
