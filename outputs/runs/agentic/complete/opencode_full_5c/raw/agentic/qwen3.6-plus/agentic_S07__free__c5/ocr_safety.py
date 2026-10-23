from typing import List, Optional
import requests
import os
from document_models import SafetyRequest, SafetyResponse, SafetyCategory


GOOGLE_PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)
GOOGLE_PERSPECTIVE_API_KEY = os.environ.get("GOOGLE_PERSPECTIVE_API_KEY", "")
GOOGLE_PERSPECTIVE_MODEL = "commentanalyzer/v1alpha1"


DEFAULT_SAFETY_CATEGORIES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
]


def check_text_safety(
    text: str,
    categories: Optional[List[str]] = None,
    threshold: float = 0.5,
) -> SafetyResponse:
    if categories is None:
        categories = DEFAULT_SAFETY_CATEGORIES
    api_key = GOOGLE_PERSPECTIVE_API_KEY
    url = f"{GOOGLE_PERSPECTIVE_API_ENDPOINT}?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {cat: {} for cat in categories},
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    attribute_scores = result.get("attributeScores", {})
    safety_categories = []
    overall_safe = True
    for attr_name, attr_data in attribute_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        is_flagged = score >= threshold
        if is_flagged:
            overall_safe = False
        safety_categories.append(
            SafetyCategory(
                name=attr_name,
                score=score,
                is_flagged=is_flagged,
            )
        )
    return SafetyResponse(
        overall_safe=overall_safe,
        categories=safety_categories,
        raw_response=result,
    )


def check_ocr_document_safety(
    text: str,
    categories: Optional[List[str]] = None,
    threshold: float = 0.3,
) -> SafetyResponse:
    if categories is None:
        categories = DEFAULT_SAFETY_CATEGORIES
    api_key = GOOGLE_PERSPECTIVE_API_KEY
    url = f"{GOOGLE_PERSPECTIVE_API_ENDPOINT}?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {cat: {} for cat in categories},
        "spanAnnotations": True,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    attribute_scores = result.get("attributeScores", {})
    safety_categories = []
    overall_safe = True
    for attr_name, attr_data in attribute_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        is_flagged = score >= threshold
        if is_flagged:
            overall_safe = False
        safety_categories.append(
            SafetyCategory(
                name=attr_name,
                score=score,
                is_flagged=is_flagged,
            )
        )
    return SafetyResponse(
        overall_safe=overall_safe,
        categories=safety_categories,
        raw_response=result,
    )


def get_safety_summary(safety_response: SafetyResponse) -> dict:
    flagged = [cat for cat in safety_response.categories if cat.is_flagged]
    return {
        "overall_safe": safety_response.overall_safe,
        "flagged_count": len(flagged),
        "flagged_categories": [cat.name for cat in flagged],
        "highest_score": max(
            (cat.score for cat in safety_response.categories), default=0.0
        ),
    }
