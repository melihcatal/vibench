"""
[SAME-SCENARIO] moderate_batch.py - Moderates a batch of user messages
and returns per-message decisions using Azure AI Content Safety.

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
from safety_models import SafetyResponse, CategoryScore, parse_raw_response, normalize_category_name


def _build_text_categories(category_names: list[str]) -> list:
    """Map string category names to Azure TextCategory enum values."""
    mapping = {
        "Hate": TextCategory.HATE,
        "SelfHarm": TextCategory.SELF_HARM,
        "Sexual": TextCategory.SEXUAL,
        "Violence": TextCategory.VIOLENCE,
    }
    return [mapping[c] for c in category_names if c in mapping]


def moderate_batch(
    messages: list[str],
    categories: Optional[list[str]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> list[SafetyResponse]:
    """
    Analyze a batch of text messages for unsafe or policy-violating content.
    Each message is analyzed independently via Azure AI Content Safety AnalyzeText.

    Returns a list of SafetyResponse objects, one per input message.
    """
    client = get_safety_client(endpoint=endpoint, api_key=api_key)
    cat_list = categories or DEFAULT_CATEGORIES
    text_categories = _build_text_categories(cat_list)

    results = []
    for idx, msg in enumerate(messages):
        try:
            options = AnalyzeTextOptions(text=msg, categories=text_categories)
            result = client.analyze_text(options)
            raw_response = {
                "id": f"batch_msg_{idx}",
                "categoriesAnalysis": [],
                "blocklistsMatch": [],
            }
            for cat in result.categories_analysis:
                raw_response["categoriesAnalysis"].append({
                    "category": cat.category,
                    "severity": cat.severity,
                })
            results.append(parse_raw_response(raw_response))
        except HttpResponseError:
            results.append(
                SafetyResponse(
                    request_id=f"batch_msg_{idx}",
                    categories=[],
                    overall_blocked=False,
                    moderation_action="error",
                )
            )
    return results


def moderate_batch_decisions(
    messages: list[str],
    severity_threshold: int = 4,
) -> list[dict]:
    """
    Return per-message allow/block decisions based on Azure AI Content Safety
    severity scores and the provided threshold.
    """
    responses = moderate_batch(messages)
    decisions = []
    for idx, (msg, resp) in enumerate(zip(messages, responses)):
        max_sev = max((c.severity for c in resp.categories), default=0)
        decisions.append({
            "index": idx,
            "text_preview": msg[:80],
            "allowed": max_sev < severity_threshold,
            "max_severity": max_sev,
            "action": resp.moderation_action,
            "category_scores": {c.category: c.severity for c in resp.categories},
        })
    return decisions


if __name__ == "__main__":
    sample_messages = [
        "Hello, how are you today?",
        "This message contains problematic content that should be reviewed.",
        "Let's schedule a meeting for tomorrow.",
    ]
    decisions = moderate_batch_decisions(sample_messages)
    for d in decisions:
        print(d)
