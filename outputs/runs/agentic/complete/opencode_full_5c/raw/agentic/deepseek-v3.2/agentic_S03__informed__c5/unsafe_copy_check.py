import os
from typing import Dict, List, Optional
import json


def unsafe_copy_check(text: str, language_code: str) -> Dict[str, any]:
    """
    Check localized copy for unsafe content using content safety API.

    Args:
        text: Text to check for unsafe content
        language_code: Language code of the text

    Returns:
        Dictionary with safety assessment results
    """
    # Use Azure AI Content Safety API
    import requests

    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    # Construct API URL
    api_url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    # Prepare request payload
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
        "language": language_code,
    }

    headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": key}

    # Make API request
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()

    # Parse and format results
    categories_analysis = result.get("categoriesAnalysis", [])

    safety_results = {
        "provider": "azure",
        "service": "Azure AI Content Safety",
        "text_preview": text[:100] + "..." if len(text) > 100 else text,
        "language": language_code,
        "categories": {},
        "overall_safe": True,
        "block_recommended": False,
    }

    for category in categories_analysis:
        cat_name = category.get("category", "").lower()
        severity = category.get("severity", 0)

        safety_results["categories"][cat_name] = {
            "severity": severity,
            "severity_level": _get_severity_level(severity),
            "safe": severity <= 1,  # 0-1 is safe, 2-3 is unsafe
        }

        if severity >= 2:  # Medium or high severity
            safety_results["overall_safe"] = False
            if severity >= 3:  # High severity
                safety_results["block_recommended"] = True

    return safety_results


def _get_severity_level(severity: int) -> str:
    """Convert numeric severity to text level."""
    levels = {0: "Safe", 1: "Low", 2: "Medium", 3: "High"}
    return levels.get(severity, "Unknown")
