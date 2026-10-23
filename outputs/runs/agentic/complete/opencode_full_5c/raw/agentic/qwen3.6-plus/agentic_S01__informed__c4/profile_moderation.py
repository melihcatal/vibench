import os
import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_profile_text(text: str, categories: list = None) -> dict:
    if not AZURE_CONTENT_SAFETY_ENDPOINT:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required"
        )
    if not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
    }

    body = {
        "text": text,
        "outputType": "FourSeverityLevels",
    }

    if categories:
        body["categories"] = categories

    resp = requests.post(url, json=body, headers=headers, timeout=30)
    resp.raise_for_status()
    result = resp.json()

    return result


def is_profile_safe(text: str, max_severity: int = 2) -> dict:
    result = moderate_profile_text(text)
    categories_result = result.get("categoriesAnalysis", [])
    flagged = []
    for cat in categories_result:
        severity = cat.get("severity", 0)
        if severity > max_severity:
            flagged.append(
                {
                    "category": cat.get("category", ""),
                    "severity": severity,
                }
            )

    is_safe = len(flagged) == 0
    return {
        "is_safe": is_safe,
        "flagged_categories": flagged,
        "raw_result": result,
    }
