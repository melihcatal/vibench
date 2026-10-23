"""
Check message payload text for unsafe content using Azure AI Content Safety.

Uses the Azure AI Content Safety REST API to analyze text from Pub/Sub
message payloads for harmful content. Authenticated via
AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY.
"""

import os
import json
import requests
from typing import Any


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://default-content-safety.cognitiveservices.azure.com",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_message_safety(
    text: str,
    categories: list[str] | None = None,
) -> dict[str, Any]:
    """
    Analyze message payload text for unsafe content categories using
    Azure AI Content Safety.

    Args:
        text: The message payload text to analyze.
        categories: Optional list of categories to check. Defaults to
                    ["Hate", "SelfHarm", "Sexual", "Violence"].

    Returns:
        Dictionary with safety analysis results including per-category
        severity levels and an overall safe/unsafe flag.
    """
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "categories": categories,
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    data = response.json()
    results: dict[str, Any] = {
        "safe": True,
        "categories": {},
        "raw_response": data,
    }

    for category_result in data.get("categoriesAnalysis", []):
        cat_name = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        results["categories"][cat_name] = {
            "severity": severity,
            "flagged": severity >= 4,
        }
        if severity >= 4:
            results["safe"] = False

    return results


def check_payload_safety(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Extract text fields from a message payload and check each for unsafe content.

    Args:
        payload: The message payload dictionary to scan.

    Returns:
        Dictionary with safety results per text field found in the payload.
    """
    text_fields: dict[str, str] = {}
    for key, value in payload.items():
        if isinstance(value, str) and len(value.strip()) > 0:
            text_fields[key] = value

    field_results: dict[str, Any] = {}
    overall_safe = True

    for field_name, field_text in text_fields.items():
        result = check_message_safety(field_text)
        field_results[field_name] = result
        if not result.get("safe", True):
            overall_safe = False

    return {
        "safe": overall_safe,
        "fields_analyzed": len(text_fields),
        "field_results": field_results,
    }


if __name__ == "__main__":
    sample_text = "This is a normal message with no harmful content."
    result = check_message_safety(sample_text)
    print(json.dumps(result, indent=2))
