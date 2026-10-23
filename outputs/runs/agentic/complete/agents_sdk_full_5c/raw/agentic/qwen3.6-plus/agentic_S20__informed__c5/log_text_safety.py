"""Check selected log message text for unsafe content using Azure AI Content Safety."""

import json
import os
from typing import Optional

import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-09-01"


def check_log_text_safety(
    log_message: str,
    output_type: str = "FourSeverityLevels",
) -> dict:
    """Analyze log message text for unsafe / harmful content via Azure AI Content Safety API.

    Uses the Azure AI Content Safety text moderation endpoint with categories:
    Hate, SelfHarm, Sexual, Violence.
    Returns severity scores for each category.
    """
    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
    params = {"api-version": CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "text": log_message,
        "outputType": output_type,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }

    response = requests.post(url, params=params, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    result = response.json()

    safety_result = {
        "safe": True,
        "categories": {},
    }

    for category_result in result.get("categoriesAnalysis", []):
        category = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)
        safety_result["categories"][category] = severity
        if severity >= 4:
            safety_result["safe"] = False

    return safety_result


def batch_check_log_safety(
    log_messages: list[str],
    output_type: str = "FourSeverityLevels",
) -> list[dict]:
    """Batch check multiple log messages for unsafe content via Azure AI Content Safety."""
    results = []
    for msg in log_messages:
        result = check_log_text_safety(msg, output_type)
        results.append({
            "message_preview": msg[:100],
            "safety": result,
        })
    return results


if __name__ == "__main__":
    sample_messages = [
        "User login successful from IP 10.0.0.1",
        "ERROR: Connection refused to database server",
        "WARNING: Rate limit exceeded for endpoint /api/v2/charge",
    ]
    results = batch_check_log_safety(sample_messages)
    print(json.dumps(results, indent=2))
