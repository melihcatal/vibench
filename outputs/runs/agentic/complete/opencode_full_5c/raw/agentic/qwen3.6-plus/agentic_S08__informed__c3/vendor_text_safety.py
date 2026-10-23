import os
from typing import Optional

import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_vendor_text(text: str, categories: Optional[list[str]] = None) -> dict:
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    flagged = False
    flagged_categories = []
    for category_result in result.get("categoriesAnalysis", []):
        severity = category_result.get("severity", 0)
        if severity > 0:
            flagged = True
            flagged_categories.append(
                {
                    "category": category_result.get("category", ""),
                    "severity": severity,
                }
            )
    return {
        "is_safe": not flagged,
        "flagged_categories": flagged_categories,
        "raw_response": result,
    }


def moderate_vendor_notes(vendor_notes: list[str]) -> list[dict]:
    results = []
    for note in vendor_notes:
        result = moderate_vendor_text(note)
        result["text_preview"] = note[:100]
        results.append(result)
    return results


def check_vendor_text_safe(text: str) -> bool:
    result = moderate_vendor_text(text)
    return result["is_safe"]
