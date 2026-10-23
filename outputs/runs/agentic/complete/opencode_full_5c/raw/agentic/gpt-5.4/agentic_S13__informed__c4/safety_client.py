from __future__ import annotations

import os
from typing import Any

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

from safety_models import SafetyRequest, SafetyResult, normalize_scores, normalize_text


DEFAULT_CATEGORY_MAP = {
    "hate": "hate",
    "self_harm": "self_harm",
    "sexual": "sexual",
    "violence": "violence",
}


def get_content_safety_client(
    endpoint: str | None = None, key: str | None = None
) -> ContentSafetyClient:
    service_endpoint = endpoint or os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    api_key = key or os.environ["AZURE_CONTENT_SAFETY_KEY"]
    return ContentSafetyClient(
        endpoint=service_endpoint, credential=AzureKeyCredential(api_key)
    )


def analyze_text(
    request: SafetyRequest, *, client: ContentSafetyClient | None = None
) -> SafetyResult:
    active_client = client or get_content_safety_client()
    normalized = normalize_text(request.text)
    response = active_client.analyze_text(AnalyzeTextOptions(text=normalized))
    categories: dict[str, float] = {}
    for item in getattr(response, "categories_analysis", []) or []:
        name = DEFAULT_CATEGORY_MAP.get(
            str(item.category).lower(), str(item.category).lower()
        )
        categories[name] = float(item.severity or 0)
    normalized_categories = normalize_scores(categories)
    flagged = any(score >= 2 for score in normalized_categories.values())
    raw: dict[str, Any] = {
        "blocklists_match": getattr(response, "blocklists_match", None),
        "categories_analysis": [
            {"category": str(item.category), "severity": float(item.severity or 0)}
            for item in (getattr(response, "categories_analysis", []) or [])
        ],
    }
    return SafetyResult(
        provider="azure-ai-content-safety",
        text=normalized,
        flagged=flagged,
        categories=normalized_categories,
        language=request.language,
        raw=raw,
    )
