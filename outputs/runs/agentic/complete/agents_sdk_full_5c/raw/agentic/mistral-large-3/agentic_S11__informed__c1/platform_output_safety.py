import os
import requests
from typing import Dict, Any
from pydantic import BaseModel


class SafetyCheckResult(BaseModel):
    is_safe: bool
    categories: Dict[str, bool]
    scores: Dict[str, float]


def check_output_safety(text: str) -> SafetyCheckResult:
    """
    Checks model output for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    body = {
        "text": text,
        "categories": ["Hate", "Sexual", "SelfHarm", "Violence"],
        "outputType": "FourSeverityLevels"
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    result = response.json()

    categories = {
        category["category"]: any(score["severity"] > 0 for score in category["severities"])
        for category in result["categoriesAnalysis"]
    }

    scores = {
        category["category"]: max(score["severity"] for score in category["severities"])
        for category in result["categoriesAnalysis"]
    }

    return SafetyCheckResult(
        is_safe=all(not flag for flag in categories.values()),
        categories=categories,
        scores=scores
    )