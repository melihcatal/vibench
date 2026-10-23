import os
import requests

from vision_models import (
    TextSafetyRequest,
    TextSafetyResponse,
    TextSafetyScore,
)


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT", ""
).rstrip("/")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_text_safety(request: TextSafetyRequest) -> TextSafetyResponse:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set"
        )

    url = f"{AZURE_CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze"
    params = {"api-version": CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    body = {
        "text": request.text,
        "categories": request.categories,
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, params=params, headers=headers, json=body, timeout=30)
    response.raise_for_status()

    data = response.json()

    scores = []
    is_safe = True
    for cat_result in data.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        score = severity / 4.0
        scores.append(TextSafetyScore(category=cat_name, score=score))
        if severity >= 2:
            is_safe = False

    return TextSafetyResponse(
        is_safe=is_safe,
        scores=scores,
        model="azure-content-safety",
    )


def check_visual_labels_safety(
    labels_text: str,
    categories: list = None,
) -> TextSafetyResponse:
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    request = TextSafetyRequest(
        text=labels_text,
        categories=categories,
    )
    return check_text_safety(request)


def check_description_safety(
    description: str,
    categories: list = None,
) -> TextSafetyResponse:
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    request = TextSafetyRequest(
        text=description,
        categories=categories,
    )
    return check_text_safety(request)
