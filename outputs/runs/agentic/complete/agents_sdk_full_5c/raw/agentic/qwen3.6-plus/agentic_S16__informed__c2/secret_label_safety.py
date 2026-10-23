"""Check secret labels and notes for unsafe text using Azure AI Content Safety.

Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
import re
import requests

from security_models import SecretFetchResponse


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

CONTENT_SAFETY_ANALYZE_URL = f"{AZURE_CONTENT_SAFETY_ENDPOINT.rstrip('/')}/contentsafety/text:analyze?api-version=2024-02-15-preview"


def check_secret_labels_safety(
    labels: list[str] | None = None,
    notes: str | None = None,
) -> dict:
    """Check secret labels and notes for unsafe content using Azure AI Content Safety.

    Returns a dict with safety analysis results per category:
      - Hate, SelfHarm, Sexual, Violence
    """
    text = _build_check_text(labels, notes)
    if not text:
        return {"status": "no_content", "safe": True, "categories": {}}

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            CONTENT_SAFETY_ANALYZE_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        categories = {}
        for cat_result in result.get("categoriesAnalysis", []):
            category = cat_result.get("category", "")
            severity = cat_result.get("severity", 0)
            categories[category] = {
                "severity": severity,
                "flagged": severity >= 2,
            }

        overall_safe = not any(c.get("flagged") for c in categories.values())

        return {
            "status": "analyzed",
            "safe": overall_safe,
            "categories": categories,
            "provider": "azure_ai_content_safety",
            "analyzed_text_length": len(text),
        }

    except requests.RequestException as exc:
        return {
            "status": "error",
            "safe": None,
            "error": str(exc),
            "provider": "azure_ai_content_safety",
        }


def _build_check_text(labels: list[str] | None, notes: str | None) -> str:
    """Combine labels and notes into a single text for safety analysis."""
    parts = []
    if labels:
        parts.append("Labels: " + ", ".join(labels))
    if notes:
        parts.append(f"Notes: {notes}")
    return " | ".join(parts)


def check_response_safety(response: SecretFetchResponse) -> dict:
    """Check the metadata notes from a SecretFetchResponse for unsafe content."""
    metadata = response.metadata or {}
    labels = metadata.get("labels", [])
    notes = metadata.get("notes", "")
    return check_secret_labels_safety(labels=labels, notes=notes)


if __name__ == "__main__":
    result = check_secret_labels_safety(
        labels=["prod", "api-key"],
        notes="This secret contains production credentials for the payment gateway.",
    )
    print(f"Safe: {result.get('safe')}")
    print(f"Categories: {result.get('categories')}")
