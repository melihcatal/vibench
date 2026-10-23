import os
import requests
from typing import Optional


def check_log_text_safety(
    text: str,
    categories: list = None,
) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    api_version = "2024-02-15-preview"

    url = f"{endpoint}/contentsafety/text:analyze?api-version={api_version}"

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": api_key,
    }

    payload = {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    result = response.json()

    analysis = {
        "text_analyzed": text,
        "has_unsafe_content": False,
        "categories": {},
        "blocklists_match": result.get("blocklistsMatch", []),
    }

    for category_result in result.get("categoriesAnalysis", []):
        cat = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        analysis["categories"][cat] = severity
        if severity > 0:
            analysis["has_unsafe_content"] = True

    return analysis
