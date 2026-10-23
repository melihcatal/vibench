"""
ocr_safety.py - Check extracted document text for unsafe content
using Azure AI Content Safety.

Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://your-content-safety-resource.cognitiveservices.azure.com/"
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")


def check_text_safety(text: str) -> dict:
    """
    Check extracted document text for unsafe content categories using
    Azure AI Content Safety text analysis API.

    Args:
        text: The text content to analyze for safety.

    Returns:
        dict with safety category scores and a summary verdict.
    """
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError(
            "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
        )

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "categories": [
            "Hate",
            "SelfHarm",
            "Sexual",
            "Violence",
        ],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()

    category_scores = {}
    for category_result in result.get("categoriesAnalysis", []):
        category_name = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        category_scores[category_name] = severity

    max_severity = max(category_scores.values()) if category_scores else 0

    verdict = "safe"
    if max_severity >= 4:
        verdict = "unsafe"
    elif max_severity >= 2:
        verdict = "review"

    return {
        "category_scores": category_scores,
        "max_severity": max_severity,
        "verdict": verdict,
    }


def check_text_safety_batch(texts: list[str]) -> list[dict]:
    """
    Check multiple text strings for unsafe content using Azure AI Content Safety.

    Args:
        texts: List of text strings to analyze.

    Returns:
        List of safety analysis results.
    """
    results = []
    for text in texts:
        results.append(check_text_safety(text))
    return results
