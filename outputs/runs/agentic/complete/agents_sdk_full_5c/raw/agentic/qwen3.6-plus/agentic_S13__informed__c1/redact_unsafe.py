"""
[SAME-SCENARIO] redact_unsafe.py - Flags or redacts unsafe spans from text
using Azure AI Content Safety for detection and local redaction logic.

Provider: Azure AI Content Safety
SDK: azure-ai-contentsafety
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

import re
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
)
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from safety_client import get_safety_client, DEFAULT_CATEGORIES
from safety_models import SafetyResponse, parse_raw_response


REDACTION_MARKERS = {
    "hate": "[HATE_REDACTED]",
    "self_harm": "[SELF_HARM_REDACTED]",
    "sexual": "[SEXUAL_REDACTED]",
    "violence": "[VIOLENCE_REDACTED]",
}


def _build_text_categories(category_names: list[str]) -> list:
    mapping = {
        "Hate": TextCategory.HATE,
        "SelfHarm": TextCategory.SELF_HARM,
        "Sexual": TextCategory.SEXUAL,
        "Violence": TextCategory.VIOLENCE,
    }
    return [mapping[c] for c in category_names if c in mapping]


def _find_unsafe_spans(
    text: str,
    response: SafetyResponse,
    severity_threshold: int = 3,
) -> list[tuple[str, int, int]]:
    """
    Identify approximate unsafe spans in the text based on which categories
    exceeded the severity threshold. Returns list of (category, start, end).
    """
    spans = []
    for cat_score in response.categories:
        if cat_score.severity >= severity_threshold:
            spans.append((cat_score.category, 0, len(text)))
    return spans


def redact_text(
    text: str,
    categories: Optional[list[str]] = None,
    severity_threshold: int = 3,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """
    Analyze text with Azure AI Content Safety and redact content that
    exceeds the severity threshold for any unsafe category.

    Returns a dict with:
      - original: the input text
      - redacted: text with unsafe spans replaced
      - flags: list of flagged categories
      - was_modified: whether any redaction occurred
    """
    client = get_safety_client(endpoint=endpoint, api_key=api_key)
    cat_list = categories or DEFAULT_CATEGORIES
    text_categories = _build_text_categories(cat_list)

    options = AnalyzeTextOptions(text=text, categories=text_categories)
    try:
        result = client.analyze_text(options)
        raw_response = {
            "id": "",
            "categoriesAnalysis": [],
            "blocklistsMatch": [],
        }
        for cat in result.categories_analysis:
            raw_response["categoriesAnalysis"].append({
                "category": cat.category,
                "severity": cat.severity,
            })
        response = parse_raw_response(raw_response)
    except HttpResponseError:
        return {
            "original": text,
            "redacted": text,
            "flags": [],
            "was_modified": False,
            "error": "moderation_api_error",
        }

    flags = []
    redacted = text
    for cat_score in response.categories:
        if cat_score.severity >= severity_threshold:
            flags.append(cat_score.category)
            marker = REDACTION_MARKERS.get(cat_score.category, "[REDACTED]")
            redacted = marker

    return {
        "original": text,
        "redacted": redacted,
        "flags": flags,
        "was_modified": len(flags) > 0,
        "category_severities": {c.category: c.severity for c in response.categories},
    }


def flag_text(
    text: str,
    severity_threshold: int = 3,
) -> dict:
    """
    Only flag text without modifying it. Returns category-level details
    from Azure AI Content Safety analysis.
    """
    result = redact_text(text, severity_threshold=severity_threshold)
    return {
        "flagged": result["was_modified"],
        "flags": result["flags"],
        "category_severities": result.get("category_severities", {}),
    }


if __name__ == "__main__":
    sample = "This text needs to be checked for unsafe content."
    result = redact_text(sample)
    print(result)
