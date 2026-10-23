import os
import requests
from translation_models import UnsafeContentCheckRequest
import dataclasses


@dataclasses.dataclass
class UnsafeContentCheckResponse:
    is_unsafe: bool
    categories: dict
    severity: dict


def check_unsafe_copy(request: UnsafeContentCheckRequest) -> UnsafeContentCheckResponse:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "text": request.text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "blocklistNames": [],
        "outputType": "FourHateCategories",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    is_unsafe = False
    categories = {}
    severity = {}

    for category_result in result.get("categoriesAnalysis", []):
        category = category_result["category"]
        severity_level = category_result["severity"]
        categories[category] = severity_level > 0
        severity[category] = severity_level
        if severity_level > 0:
            is_unsafe = True

    return UnsafeContentCheckResponse(
        is_unsafe=is_unsafe, categories=categories, severity=severity
    )
