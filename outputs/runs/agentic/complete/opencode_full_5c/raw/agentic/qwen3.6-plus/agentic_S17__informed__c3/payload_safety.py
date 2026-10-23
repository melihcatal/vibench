import os
import logging
from typing import Optional, Dict, List

import requests

from security_models import SafetyCheckResult

logger = logging.getLogger(__name__)

AZURE_CONTENT_SAFETY_SERVICE = "Azure AI Content Safety"
AZURE_CONTENT_SAFETY_ENDPOINT_ENV = "AZURE_CONTENT_SAFETY_ENDPOINT"
AZURE_CONTENT_SAFETY_KEY_ENV = "AZURE_CONTENT_SAFETY_KEY"
AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"

HAZARD_CATEGORIES = ["Hate", "SelfHarm", "Sexual", "Violence"]


def check_payload_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = AZURE_CONTENT_SAFETY_API_VERSION,
    categories: Optional[List[str]] = None,
    threshold: int = 4,
) -> SafetyCheckResult:
    endpoint = endpoint or os.environ[AZURE_CONTENT_SAFETY_ENDPOINT_ENV].rstrip("/")
    key = api_key or os.environ[AZURE_CONTENT_SAFETY_KEY_ENV]
    categories_to_check = categories or HAZARD_CATEGORIES

    url = f"{endpoint}/contentsafety/text:analyze"
    params = {"api-version": api_version}
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "categories": categories_to_check,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, params=params, headers=headers, json=body, timeout=30)
    response.raise_for_status()

    data = response.json()

    category_scores: Dict[str, float] = {}
    flagged: List[str] = []

    for category_result in data.get("categoriesAnalysis", []):
        cat_name = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        normalized_score = severity / 7.0
        category_scores[cat_name] = normalized_score
        if severity >= threshold:
            flagged.append(cat_name)

    is_safe = len(flagged) == 0
    overall_score = max(category_scores.values()) if category_scores else 0.0

    details_parts = []
    for cat, score in category_scores.items():
        status = "FLAGGED" if cat in flagged else "OK"
        details_parts.append(f"{cat}: {score:.2f} [{status}]")

    result = SafetyCheckResult(
        is_safe=is_safe,
        categories=category_scores,
        flagged_categories=flagged,
        overall_score=overall_score,
        details="; ".join(details_parts),
    )

    logger.info(
        "Checked payload safety with %s: safe=%s, flagged=%s",
        AZURE_CONTENT_SAFETY_SERVICE,
        result.is_safe,
        result.flagged_categories,
    )

    return result


def check_multiple_payloads(
    texts: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    threshold: int = 4,
) -> List[SafetyCheckResult]:
    results = []
    for text in texts:
        result = check_payload_safety(
            text=text,
            endpoint=endpoint,
            api_key=api_key,
            threshold=threshold,
        )
        results.append(result)
    return results
