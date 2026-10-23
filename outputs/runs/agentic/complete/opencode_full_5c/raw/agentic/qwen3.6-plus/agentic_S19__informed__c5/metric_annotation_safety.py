from __future__ import annotations

import os
from typing import Any

import requests


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<resource-name>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_metric_annotation_safety(
    text: str,
    categories: list[str] | None = None,
) -> dict[str, Any]:
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    payload = {
        "text": text,
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }
    resp = requests.post(url, headers=headers, params=params, json=payload, timeout=30)
    resp.raise_for_status()
    body = resp.json()
    results = body.get("categoriesAnalysis", [])
    flagged = []
    for cat_result in results:
        category = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        if severity > 0:
            flagged.append({"category": category, "severity": severity})
    return {
        "text": text,
        "service": "Azure AI Content Safety",
        "flagged_categories": flagged,
        "is_safe": len(flagged) == 0,
        "raw_response": body,
    }
