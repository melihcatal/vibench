import os
from typing import Optional

import requests

from safety_models import (
    SafetyCategory,
    SeverityLevel,
    SafetyRequest,
    SafetyResponse,
    CategoryScore,
)

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT", ""
).rstrip("/")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
API_VERSION = "2024-02-15-preview"

CATEGORY_MAP = {
    "Hate": SafetyCategory.HATE,
    "SelfHarm": SafetyCategory.SELF_HARM,
    "Sexual": SafetyCategory.SEXUAL,
    "Violence": SafetyCategory.VIOLENCE,
}

SEVERITY_MAP = {
    0: SeverityLevel.SAFE,
    2: SeverityLevel.LOW,
    4: SeverityLevel.MEDIUM,
    6: SeverityLevel.HIGH,
}


def get_azure_endpoint() -> str:
    if not AZURE_CONTENT_SAFETY_ENDPOINT:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required"
        )
    return AZURE_CONTENT_SAFETY_ENDPOINT


def get_azure_key() -> str:
    if not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")
    return AZURE_CONTENT_SAFETY_KEY


def build_payload(request: SafetyRequest) -> dict:
    return {
        "text": request.text,
        "categories": [c.value for c in request.categories],
        "outputType": request.output_type,
    }


def parse_response(
    text: str, raw: dict, categories: list[SafetyCategory]
) -> SafetyResponse:
    category_scores = []
    block_action = False

    for cat_result in raw.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity_val = cat_result.get("severity", 0)
        severity = SEVERITY_MAP.get(severity_val, SeverityLevel.SAFE)

        try:
            category = SafetyCategory(cat_name)
        except ValueError:
            continue

        if category not in categories:
            continue

        severity_score = severity.value / 6.0
        category_scores.append(
            CategoryScore(
                category=category,
                severity=severity,
                raw_score=severity_score,
            )
        )

        if severity.value >= SeverityLevel.MEDIUM.value:
            block_action = True

    return SafetyResponse(
        text=text,
        category_scores=category_scores,
        block_action=block_action,
        raw_response=raw,
    )


def normalize_scores(
    scores: list[CategoryScore],
) -> dict[SafetyCategory, float]:
    return {score.category: score.raw_score for score in scores}


def call_azure_content_safety(
    request: SafetyRequest,
    timeout: int = 30,
) -> SafetyResponse:
    endpoint = get_azure_endpoint()
    key = get_azure_key()
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    payload = build_payload(request)

    response = requests.post(
        url, params=params, headers=headers, json=payload, timeout=timeout
    )
    response.raise_for_status()
    raw = response.json()

    return parse_response(request.text, raw, request.categories)


def call_azure_content_safety_batch(
    texts: list[str],
    categories: list[SafetyCategory],
    timeout: int = 30,
) -> list[dict]:
    endpoint = get_azure_endpoint()
    key = get_azure_key()
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    results = []
    for text in texts:
        payload = {
            "text": text,
            "categories": [c.value for c in categories],
            "outputType": "FourSeverityLevels",
        }
        response = requests.post(
            url, params=params, headers=headers, json=payload, timeout=timeout
        )
        response.raise_for_status()
        results.append(response.json())

    return results
