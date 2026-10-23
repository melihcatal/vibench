"""
[SAME-SCENARIO] moderate_text.py - Scores user text for unsafe or policy-violating content
using Azure AI Content Safety service.

Provider: Azure AI Content Safety
SDK: azure-ai-contentsafety
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import os
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
)
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from safety_client import get_safety_client, DEFAULT_CATEGORIES
from safety_models import SafetyRequest, SafetyResponse, CategoryScore, parse_raw_response, normalize_category_name


def moderate_text(
    text: str,
    categories: Optional[list[str]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> SafetyResponse:
    """
    Analyze a single text string for unsafe or policy-violating content
    using Azure AI Content Safety (AnalyzeText API).

    Returns a normalized SafetyResponse with per-category severity scores.
    """
    client = get_safety_client(endpoint=endpoint, api_key=api_key)
    cat_list = categories or DEFAULT_CATEGORIES

    text_categories = []
    for cat_name in cat_list:
        text_categories.append(TextCategory.HATE) if cat_name == "Hate" else None
        if cat_name == "SelfHarm":
            text_categories.append(TextCategory.SELF_HARM)
        elif cat_name == "Sexual":
            text_categories.append(TextCategory.SEXUAL)
        elif cat_name == "Violence":
            text_categories.append(TextCategory.VIOLENCE)
        elif cat_name == "Hate":
            text_categories.append(TextCategory.HATE)

    options = AnalyzeTextOptions(text=text, categories=text_categories)

    try:
        result = client.analyze_text(options)
        raw_response = {
            "id": getattr(result, "id", ""),
            "categoriesAnalysis": [],
            "blocklistsMatch": [],
        }
        for cat in result.categories_analysis:
            raw_response["categoriesAnalysis"].append({
                "category": cat.category,
                "severity": cat.severity,
            })
        return parse_raw_response(raw_response)
    except HttpResponseError as e:
        return SafetyResponse(
            request_id="",
            categories=[],
            overall_blocked=False,
            moderation_action="error",
        )


def moderate_text_safe(
    text: str,
    threshold: int = 4,
) -> dict:
    """
    Convenience wrapper that returns a simple safe/unsafe decision.
    Uses Azure AI Content Safety default categories and severity threshold.
    """
    response = moderate_text(text)
    is_unsafe = any(c.severity >= threshold for c in response.categories)
    return {
        "text": text[:100],
        "safe": not is_unsafe,
        "max_severity": max((c.severity for c in response.categories), default=0),
        "categories": {c.category: c.severity for c in response.categories},
        "action": response.moderation_action,
    }


if __name__ == "__main__":
    sample_text = os.environ.get("SAMPLE_TEXT", "This is a sample text for moderation.")
    result = moderate_text_safe(sample_text)
    print(result)
