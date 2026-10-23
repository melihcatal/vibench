import json
import os
import requests
from typing import Optional


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_message_safety(
    text: str,
    categories: Optional[list[str]] = None,
) -> dict:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        return {
            "success": False,
            "error": "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required",
            "safe": True,
        }

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    endpoint_url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    payload = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            endpoint_url, headers=headers, params=params, json=payload, timeout=30
        )
        response.raise_for_status()
        result = response.json()

        category_scores = {}
        max_severity = 0
        for category_result in result.get("categoriesAnalysis", []):
            cat = category_result.get("category", "")
            severity = category_result.get("severity", 0)
            category_scores[cat] = severity
            max_severity = max(max_severity, severity)

        is_safe = max_severity <= 2

        return {
            "success": True,
            "safe": is_safe,
            "category_scores": category_scores,
            "max_severity": max_severity,
            "service": "Azure AI Content Safety",
        }
    except requests.exceptions.RequestException as exc:
        return {
            "success": False,
            "error": str(exc),
            "safe": True,
        }


def main():
    sample_text = os.environ.get(
        "MESSAGE_TEXT", "This is a normal customer message with no issues."
    )
    result = check_message_safety(sample_text)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
