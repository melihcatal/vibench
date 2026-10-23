import os
import json
from typing import Optional

AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_vendor_text(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    categories: Optional[list] = None,
) -> dict:
    endpoint = endpoint or os.environ.get(AZURE_CONTENT_SAFETY_ENDPOINT_ENV, "")
    api_key = api_key or os.environ.get(AZURE_CONTENT_SAFETY_KEY_ENV, "")

    if not endpoint:
        raise ValueError(
            f"Azure Content Safety endpoint not found. Set {AZURE_CONTENT_SAFETY_ENDPOINT_ENV}."
        )
    if not api_key:
        raise ValueError(
            f"Azure Content Safety key not found. Set {AZURE_CONTENT_SAFETY_KEY_ENV}."
        )

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    import requests

    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, headers=headers, params=params, json=payload)
    response.raise_for_status()
    result = response.json()

    flagged_categories = []
    highest_severity = 0

    for category_result in result.get("categoriesAnalysis", []):
        severity = category_result.get("severity", 0)
        if severity > 0:
            flagged_categories.append(
                {
                    "category": category_result.get("category", ""),
                    "severity": severity,
                }
            )
        highest_severity = max(highest_severity, severity)

    is_safe = highest_severity <= 2

    return {
        "success": True,
        "is_safe": is_safe,
        "text": text,
        "highest_severity": highest_severity,
        "flagged_categories": flagged_categories,
        "provider": "azure-content-safety",
        "endpoint": endpoint,
    }


def moderate_vendor_notes(
    invoice_notes: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    if not invoice_notes or not invoice_notes.strip():
        return {
            "success": True,
            "is_safe": True,
            "text": invoice_notes,
            "highest_severity": 0,
            "flagged_categories": [],
            "provider": "azure-content-safety",
            "note": "Empty or whitespace-only text is considered safe.",
        }

    return moderate_vendor_text(invoice_notes, endpoint=endpoint, api_key=api_key)


if __name__ == "__main__":
    sample_text = (
        "Payment for office supplies delivered on time. Thank you for your business."
    )
    result = moderate_vendor_notes(sample_text)
    print(json.dumps(result, indent=2))
