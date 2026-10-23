from __future__ import annotations

import os
from typing import Any

import requests
from database_models import DocumentResponse

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
API_VERSION = "2024-02-15-preview"


def check_text_safety(
    documents: list[DocumentResponse],
    categories: list[str] | None = None,
) -> dict[str, Any]:
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    results = {}

    for doc in documents:
        text_fields = _extract_text_fields(doc.data)
        doc_safety = {}

        for field_name, text in text_fields.items():
            payload = {
                "text": text,
                "categories": categories,
                "outputType": "EightSeverityLevels",
            }

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            analysis = response.json()

            doc_safety[field_name] = {
                "categories": {
                    cat["category"]: {
                        "severity": cat.get("severity", 0),
                        "severityLabel": cat.get("severityLabel", "Unknown"),
                    }
                    for cat in analysis.get("categoriesAnalysis", [])
                },
                "blocklistsMatch": analysis.get("blocklistsMatch", []),
            }

        results[doc.document_id] = doc_safety

    return results


def _extract_text_fields(data: dict[str, Any]) -> dict[str, str]:
    text_fields = {}
    for key, value in data.items():
        if isinstance(value, str) and len(value) > 0:
            text_fields[key] = value
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, str) and len(sub_value) > 0:
                    text_fields[f"{key}.{sub_key}"] = sub_value
    return text_fields
