"""
script_safety.py - Check narration scripts for unsafe content.

Uses the Azure Content Safety API (Cognitive Services) to analyze
narration scripts for unsafe content before sending them to TTS synthesis.
Provider: Microsoft Azure Cognitive Services Content Safety API
Endpoint: https://{resource-name}.cognitiveservices.azure.com/contentmoderator/moderate/v1.0
"""

import os
import requests
from typing import Optional, List, Dict, Any

from speech_models import TTSRequest


# Azure Content Safety API configuration
AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://api.cognitive.microsoft.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")


class SafetyResult:
    """Result from Azure Content Safety analysis."""

    def __init__(
        self,
        is_safe: bool,
        categories: Dict[str, float],
        flagged_categories: List[str],
        severity: float,
        raw_response: Optional[Dict[str, Any]] = None,
    ):
        self.is_safe = is_safe
        self.categories = categories
        self.flagged_categories = flagged_categories
        self.severity = severity
        self.raw_response = raw_response

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "is_safe": self.is_safe,
            "categories": self.categories,
            "flagged_categories": self.flagged_categories,
            "severity": self.severity,
        }


def check_script_safety(
    text: str,
    subscription_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    categories: Optional[List[str]] = None,
) -> SafetyResult:
    """
    Check a narration script for unsafe content using Azure Content Safety API.

    Analyzes text for hate, violence, self-harm, and sexual content categories
    using Azure's Content Safety service before allowing TTS synthesis.

    Args:
        text: Narration script text to analyze.
        subscription_key: Azure Content Safety subscription key.
        endpoint: Azure Content Safety endpoint URL.
        categories: List of categories to check (defaults to all four).

    Returns:
        SafetyResult with category scores and safety verdict.
    """
    key = subscription_key or AZURE_CONTENT_SAFETY_KEY
    base_endpoint = endpoint or AZURE_CONTENT_SAFETY_ENDPOINT

    if not key:
        return SafetyResult(
            is_safe=False,
            categories={},
            flagged_categories=["UNABLE_TO_CHECK"],
            severity=1.0,
        )

    # Azure Content Safety Text Analysis endpoint
    safety_endpoint = f"{base_endpoint.rstrip('/')}/contentsafety/text:analyze"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    check_categories = categories or ["Hate", "Sexual", "SelfHarm", "Violence"]

    body = {
        "text": text,
        "categories": check_categories,
        "outputType": "EightSeverityLevels",
    }

    try:
        response = requests.post(
            safety_endpoint,
            headers=headers,
            json=body,
            params={"api-version": "2023-10-01"},
            timeout=15,
        )
        response.raise_for_status()

        result_data = response.json()
        return _parse_safety_response(result_data)

    except requests.exceptions.RequestException as exc:
        return SafetyResult(
            is_safe=False,
            categories={},
            flagged_categories=["API_ERROR"],
            severity=1.0,
            raw_response={"error": str(exc)},
        )


def validate_tts_request_safety(
    request: TTSRequest,
    subscription_key: Optional[str] = None,
    endpoint: Optional[str] = None,
    max_severity: int = 4,
) -> Dict[str, Any]:
    """
    Validate a TTS request's text content for safety using Azure Content Safety.

    Checks the text content of a TTS request against Azure's content safety
    categories and returns a validation result.

    Args:
        request: TTSRequest to validate.
        subscription_key: Azure Content Safety subscription key.
        endpoint: Azure Content Safety endpoint URL.
        max_severity: Maximum allowed severity level (1-7).

    Returns:
        Dictionary with validation status and details.
    """
    result = check_script_safety(
        text=request.text,
        subscription_key=subscription_key,
        endpoint=endpoint,
    )

    is_approved = result.is_safe and result.severity <= max_severity

    return {
        "approved": is_approved,
        "voice_name": request.voice_name,
        "locale": request.locale,
        "safety_check": result.to_dict(),
        "reason": "Content flagged by Azure Content Safety API" if not is_approved else None,
    }


def batch_check_scripts(
    texts: List[str],
    subscription_key: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> List[SafetyResult]:
    """
    Check multiple narration scripts for unsafe content.

    Processes each text through Azure Content Safety API individually
    (batch endpoint support depends on API tier).

    Args:
        texts: List of narration script texts.
        subscription_key: Azure Content Safety subscription key.
        endpoint: Azure Content Safety endpoint URL.

    Returns:
        List of SafetyResult objects.
    """
    return [
        check_script_safety(text, subscription_key, endpoint)
        for text in texts
    ]


def _parse_safety_response(response_data: Dict[str, Any]) -> SafetyResult:
    """
    Parse Azure Content Safety API response into a SafetyResult.

    The Azure Content Safety API returns categories with severity values
    from 0 to 7.

    Args:
        response_data: Raw JSON response from Azure API.

    Returns:
        Parsed SafetyResult object.
    """
    categories = {}
    flagged = []
    max_severity = 0

    for category_result in response_data.get("categoriesAnalysis", []):
        category = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        categories[category] = severity

        if severity > 0:
            flagged.append(category)

        if severity > max_severity:
            max_severity = severity

    is_safe = len(flagged) == 0

    return SafetyResult(
        is_safe=is_safe,
        categories=categories,
        flagged_categories=flagged,
        severity=max_severity,
        raw_response=response_data,
    )
