"""
Check decrypted text payloads for unsafe content using Azure AI Content Safety.
Azure AI Content Safety (azure-ai-contentsafety) is the concrete provider for text moderation.

This module analyzes decrypted payloads for toxicity, hate speech, self-harm,
sexual content, and violence using Azure AI Content Safety API.
"""

import os
import json
from typing import Dict, Any, Optional, List

import requests
from requests.exceptions import RequestException


# Azure AI Content Safety endpoint configuration
AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT", "https://<your-resource>.cognitiveservices.azure.com/"
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


# Azure AI Content Safety categories
CONTENT_SAFETY_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]


def check_payload_safety(
    text: str,
    categories: Optional[List[str]] = None,
    output_type: str = "EightSeverityLevels",
    halt_on_unsafe: bool = False,
) -> Dict[str, Any]:
    """
    Check a decrypted text payload for unsafe content using Azure AI Content Safety.

    Uses Azure AI Content Safety REST API to analyze text for harmful content
    across multiple categories with severity levels.

    Args:
        text: The decrypted text payload to analyze.
        categories: List of categories to check (default: all).
        output_type: Output format (EightSeverityLevels or Binary).
        halt_on_unsafe: If True, raises exception on unsafe content detected.

    Returns:
        Dict with analysis results including categories and severity levels.

    Raises:
        ValueError: If text is empty.
        RequestException: If Azure API call fails.
        ContentUnsafeError: If halt_on_unsafe is True and content is unsafe.
    """
    if not text:
        raise ValueError("text payload cannot be empty")

    check_categories = categories or CONTENT_SAFETY_CATEGORIES

    endpoint = f"{AZURE_CONTENT_SAFETY_ENDPOINT.rstrip('/')}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categories": check_categories,
        "outputType": output_type,
    }

    try:
        response = requests.post(
            endpoint,
            params=params,
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
    except RequestException as e:
        raise RequestException(f"Azure AI Content Safety API call failed: {e}") from e

    # Parse results
    analysis_result = {
        "text_length": len(text),
        "categories_analyzed": check_categories,
        "output_type": output_type,
        "categories": {},
        "is_unsafe": False,
    }

    for category_result in result.get("categoriesAnalysis", []):
        cat_name = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        analysis_result["categories"][cat_name] = {
            "severity": severity,
            "unsafe": severity > 0,
        }
        if severity > 0:
            analysis_result["is_unsafe"] = True

    if halt_on_unsafe and analysis_result["is_unsafe"]:
        unsafe_cats = [
            cat for cat, data in analysis_result["categories"].items()
            if data["unsafe"]
        ]
        raise ContentUnsafeError(
            f"Unsafe content detected in categories: {', '.join(unsafe_cats)}"
        )

    return analysis_result


def batch_check_payloads(
    texts: List[str],
    categories: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Check multiple decrypted payloads for unsafe content.

    Args:
        texts: List of text payloads to analyze.
        categories: Categories to check.

    Returns:
        List of analysis results.
    """
    results = []
    for i, text in enumerate(texts):
        try:
            result = check_payload_safety(text, categories=categories)
            result["payload_index"] = i
            results.append(result)
        except Exception as e:
            results.append({
                "payload_index": i,
                "error": str(e),
                "is_unsafe": False,
            })
    return results


class ContentUnsafeError(Exception):
    """Raised when unsafe content is detected and halt_on_unsafe is True."""
    pass


def main():
    """CLI entry point for payload_safety."""
    text = os.environ.get("PAYLOAD_TEXT", "This is a test payload for safety checking.")
    halt_on_unsafe = os.environ.get("HALT_ON_UNSAFE", "false").lower() == "true"

    try:
        result = check_payload_safety(
            text=text,
            halt_on_unsafe=halt_on_unsafe,
        )
        print("Payload Safety Analysis (Azure AI Content Safety):")
        print(json.dumps(result, indent=2))
    except ContentUnsafeError as e:
        print(f"Unsafe content detected: {e}")
        exit(1)
    except Exception as e:
        print(f"Safety check failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
