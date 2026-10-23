import os
from typing import Optional

import requests


def check_unsafe_copy(
    text: str,
    categories: Optional[list[str]] = None,
    threshold: int = 4,
) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    check_categories = categories or [
        "Hate",
        "SelfHarm",
        "Sexual",
        "Violence",
    ]

    body = {
        "text": text,
        "categories": check_categories,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()

    flagged = []
    for category_result in result.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        if severity >= threshold:
            flagged.append(
                {
                    "category": category,
                    "severity": severity,
                    "flagged": True,
                }
            )

    is_unsafe = len(flagged) > 0

    return {
        "text_analyzed": text,
        "is_unsafe": is_unsafe,
        "flagged_categories": flagged,
        "threshold_used": threshold,
        "raw_response": result,
    }
