import os
import requests
from typing import Optional
from security_models import SafetyCheckResult


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_secret_label_safety(
    label_text: str,
    categories: Optional[list[str]] = None,
) -> SafetyCheckResult:
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": label_text,
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result_data = response.json()
    return _parse_safety_response(label_text, result_data)


def check_secret_notes_safety(
    notes_text: str,
    categories: Optional[list[str]] = None,
) -> SafetyCheckResult:
    return check_secret_label_safety(notes_text, categories)


def _parse_safety_response(text: str, result_data: dict) -> SafetyCheckResult:
    categories_scores = {}
    flagged = []
    confidence = {}
    for category_result in result_data.get("categoriesAnalysis", []):
        cat = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        categories_scores[cat] = severity
        confidence[cat] = min(severity / 7.0, 1.0)
        if severity >= 4:
            flagged.append(cat)
    is_safe = len(flagged) == 0
    return SafetyCheckResult(
        text=text,
        is_safe=is_safe,
        categories=categories_scores,
        flagged_categories=flagged,
        confidence_scores=confidence,
    )


def batch_check_labels(
    labels: list[str],
    categories: Optional[list[str]] = None,
) -> list[SafetyCheckResult]:
    return [check_secret_label_safety(label, categories) for label in labels]
