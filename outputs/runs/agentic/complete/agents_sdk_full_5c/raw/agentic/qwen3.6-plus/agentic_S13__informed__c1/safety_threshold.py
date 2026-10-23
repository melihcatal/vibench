"""
[SAME-SCENARIO] safety_threshold.py - Applies category thresholds to decide
whether to allow text using Azure AI Content Safety severity scores.

Provider: Azure AI Content Safety
SDK: azure-ai-contentsafety
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

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


DEFAULT_THRESHOLDS = {
    "hate": 4,
    "self_harm": 4,
    "sexual": 4,
    "violence": 4,
}


def _build_text_categories(category_names: list[str]) -> list:
    mapping = {
        "Hate": TextCategory.HATE,
        "SelfHarm": TextCategory.SELF_HARM,
        "Sexual": TextCategory.SEXUAL,
        "Violence": TextCategory.VIOLENCE,
    }
    return [mapping[c] for c in category_names if c in mapping]


def apply_thresholds(
    text: str,
    thresholds: Optional[dict[str, int]] = None,
    categories: Optional[list[str]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """
    Analyze text with Azure AI Content Safety and apply per-category
    severity thresholds to determine if the text should be allowed.

    Args:
        text: The text to analyze.
        thresholds: Dict mapping category names to max allowed severity.
        categories: List of Azure category names to analyze.
        endpoint: Optional Azure endpoint override.
        api_key: Optional Azure API key override.

    Returns:
        Dict with allowed (bool), violations (list), and scores (dict).
    """
    client = get_safety_client(endpoint=endpoint, api_key=api_key)
    cat_list = categories or DEFAULT_CATEGORIES
    text_categories = _build_text_categories(cat_list)
    thresholds = thresholds or DEFAULT_THRESHOLDS

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
            "allowed": True,
            "violations": [],
            "scores": {},
            "error": "moderation_api_error",
        }

    violations = []
    scores = {}
    for cat_score in response.categories:
        threshold = thresholds.get(cat_score.category, 4)
        scores[cat_score.category] = cat_score.severity
        if cat_score.severity > threshold:
            violations.append({
                "category": cat_score.category,
                "severity": cat_score.severity,
                "threshold": threshold,
                "exceeded_by": cat_score.severity - threshold,
            })

    return {
        "allowed": len(violations) == 0,
        "violations": violations,
        "scores": scores,
        "overall_action": "allow" if len(violations) == 0 else "block",
    }


def is_text_allowed(
    text: str,
    thresholds: Optional[dict[str, int]] = None,
) -> bool:
    """Simple boolean check: is the text allowed under the given thresholds?"""
    result = apply_thresholds(text, thresholds=thresholds)
    return result.get("allowed", True)


if __name__ == "__main__":
    sample = "Checking this text against safety thresholds."
    result = apply_thresholds(sample)
    print(result)
