import os
import requests
from typing import Dict, Any, Optional

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT", "https://default.cognitiveservices.azure.com/"
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_vendor_text(
    text: str,
    categories: Optional[list] = None,
) -> Dict[str, Any]:
    if not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    payload = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    flagged = False
    category_scores = {}
    for category_result in result.get("categoriesAnalysis", []):
        cat = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        category_scores[cat] = severity
        if severity > 0:
            flagged = True

    return {
        "flagged": flagged,
        "category_scores": category_scores,
        "original_text": text,
        "safe_to_use": not flagged,
    }


def moderate_vendor_notes(
    vendor_notes: str,
) -> Dict[str, Any]:
    return moderate_vendor_text(vendor_notes)


def moderate_vendor_notes_batch(
    vendor_notes_list: list,
) -> list:
    results = []
    for notes in vendor_notes_list:
        results.append(moderate_vendor_text(notes))
    return results


def filter_safe_vendor_notes(
    vendor_notes_list: list,
) -> list:
    safe_notes = []
    for notes in vendor_notes_list:
        moderation_result = moderate_vendor_text(notes)
        if moderation_result["safe_to_use"]:
            safe_notes.append(notes)
    return safe_notes
