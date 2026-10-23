import os
import time
import requests
from identity_client import AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
from identity_models import ModerationResult


AZURE_CONTENT_SAFETY_API_VERSION = os.environ.get(
    "AZURE_CONTENT_SAFETY_API_VERSION", "2024-02-15-preview"
)


def _build_moderation_url():
    base = AZURE_CONTENT_SAFETY_ENDPOINT.rstrip("/")
    return f"{base}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"


def moderate_claims_text(text, categories=None, api_key=None, endpoint=None):
    if not api_key:
        api_key = AZURE_CONTENT_SAFETY_KEY
    if not endpoint:
        endpoint = AZURE_CONTENT_SAFETY_ENDPOINT
    if not text or not text.strip():
        return ModerationResult(
            flagged=False,
            categories={},
            severity="none",
            details="Empty text provided",
        )
    url = _build_moderation_url()
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    payload = {"text": text}
    if categories:
        payload["categories"] = categories
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    results = data.get("categoriesAnalysis", [])
    categories_scores = {}
    flagged = False
    max_severity = 0
    for item in results:
        cat = item.get("category", "unknown")
        severity = item.get("severity", 0)
        categories_scores[cat] = severity
        if severity > 0:
            flagged = True
        if severity > max_severity:
            max_severity = severity
    if max_severity == 0:
        severity_label = "none"
    elif max_severity <= 2:
        severity_label = "low"
    elif max_severity <= 4:
        severity_label = "medium"
    else:
        severity_label = "high"
    return ModerationResult(
        flagged=flagged,
        categories=categories_scores,
        severity=severity_label,
        details=f"Azure AI Content Safety analyzed {len(text)} characters across {len(results)} categories",
    )


def moderate_multiple_claims(texts, categories=None, api_key=None, endpoint=None):
    results = []
    for text in texts:
        result = moderate_claims_text(text, categories, api_key, endpoint)
        results.append(result)
    return results


def is_claims_safe(text, threshold=2, api_key=None, endpoint=None):
    result = moderate_claims_text(text, api_key=api_key, endpoint=endpoint)
    return not result.flagged or all(v <= threshold for v in result.categories.values())
