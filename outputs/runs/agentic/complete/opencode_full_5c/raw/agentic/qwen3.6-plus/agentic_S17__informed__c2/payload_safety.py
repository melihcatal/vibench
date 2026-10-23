import os
import requests
from typing import Optional, Dict, List

from security_models import SafetyCheckResult

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<resource-name>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"

HAZARD_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]


def check_payload_safety(
    text: str,
    categories: Optional[List[str]] = None,
    block_threshold: int = 4,
) -> SafetyCheckResult:
    if not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    endpoint = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_CONTENT_SAFETY_KEY,
        "Content-Type": "application/json",
    }

    check_categories = categories or HAZARD_CATEGORIES
    body = {
        "text": text,
        "categories": check_categories,
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(
            url, params=params, headers=headers, json=body, timeout=30
        )
        response.raise_for_status()
        result_data = response.json()
    except requests.exceptions.HTTPError as e:
        error_detail = e.response.text if e.response else str(e)
        raise RuntimeError(
            f"Azure AI Content Safety analyze request failed (HTTP {e.response.status_code}): {error_detail}"
        ) from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Azure AI Content Safety request failed: {e}") from e

    categories_flagged = []
    severity_scores = {}

    for category_result in result_data.get("categoriesAnalysis", []):
        category_name = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        severity_scores[category_name] = severity
        if severity >= block_threshold:
            categories_flagged.append(category_name)

    is_safe = len(categories_flagged) == 0

    return SafetyCheckResult(
        is_safe=is_safe,
        categories_flagged=categories_flagged,
        severity_scores=severity_scores,
        raw_response=result_data,
    )


def check_payload_safety_with_hate_speech(
    text: str,
    block_threshold: int = 4,
) -> SafetyCheckResult:
    return check_payload_safety(
        text=text,
        categories=["Hate", "SelfHarm", "Sexual", "Violence"],
        block_threshold=block_threshold,
    )


def is_payload_safe(
    text: str,
    block_threshold: int = 4,
) -> bool:
    result = check_payload_safety(text, block_threshold=block_threshold)
    return result.is_safe


def get_safety_report(
    text: str,
    block_threshold: int = 4,
) -> Dict[str, object]:
    result = check_payload_safety(text, block_threshold=block_threshold)
    return {
        "is_safe": result.is_safe,
        "categories_flagged": result.categories_flagged,
        "severity_scores": result.severity_scores,
    }
