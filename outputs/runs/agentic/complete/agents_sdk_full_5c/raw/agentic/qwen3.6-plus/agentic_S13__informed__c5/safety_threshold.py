"""
Apply category severity thresholds to decide whether to allow or block text.
Provider: Azure AI Content Safety via azure-ai-contentsafety SDK.
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from safety_client import get_content_safety_client
from safety_models import (
    SafetyRequest,
    SafetyResponse,
    parse_azure_response,
    SafetyCategory,
    SafetySeverity,
)
from azure.core.exceptions import HttpResponseError
from typing import Optional, List, Dict


DEFAULT_THRESHOLDS = {
    SafetyCategory.HATE: SafetySeverity.LOW,
    SafetyCategory.SELF_HARM: SafetySeverity.LOW,
    SafetyCategory.SEXUAL: SafetySeverity.LOW,
    SafetyCategory.VIOLENCE: SafetySeverity.LOW,
}

SEVERITY_ORDER = [
    SafetySeverity.SAFE,
    SafetySeverity.LOW,
    SafetySeverity.MEDIUM,
    SafetySeverity.HIGH,
]


def _severity_exceeds_threshold(
    actual: SafetySeverity,
    threshold: SafetySeverity,
) -> bool:
    """Check if actual severity meets or exceeds the threshold."""
    return SEVERITY_ORDER.index(actual) >= SEVERITY_ORDER.index(threshold)


def safety_threshold(
    text: str,
    thresholds: Optional[Dict[SafetyCategory, SafetySeverity]] = None,
    default_threshold: Optional[SafetySeverity] = None,
    categories: Optional[List[SafetyCategory]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict:
    """
    Apply category thresholds to decide whether to allow or block text.

    Each category can have its own threshold. Text is allowed only if no
    category's severity meets or exceeds its threshold.

    Args:
        text: The user text to evaluate.
        thresholds: Dict mapping SafetyCategory to SafetySeverity threshold.
            If a category is not specified, uses default_threshold or LOW.
        default_threshold: Default severity threshold for unspecified categories.
        categories: Optional list of SafetyCategory to evaluate.
        endpoint: Optional Azure Content Safety endpoint override.
        api_key: Optional Azure Content Safety API key override.

    Returns:
        Dictionary with allow decision, per-category results, and violations.
    """
    if thresholds is None:
        thresholds = {}
    if default_threshold is None:
        default_threshold = SafetySeverity.LOW

    # Fill in missing categories with default threshold
    all_thresholds = {}
    for cat in [SafetyCategory.HATE, SafetyCategory.SELF_HARM,
                SafetyCategory.SEXUAL, SafetyCategory.VIOLENCE]:
        all_thresholds[cat] = thresholds.get(cat, default_threshold)

    client = get_content_safety_client(endpoint=endpoint, api_key=api_key)
    request = SafetyRequest(text=text, categories=categories)
    azure_options = request.to_azure_options()

    try:
        raw_response = client.analyze_text(options=azure_options)
        result = parse_azure_response(raw_response)
    except HttpResponseError as e:
        return {
            "allow": False,
            "violations": [],
            "categories": [],
            "error": str(e),
        }

    violations = []
    category_decisions = []

    for cat_score in result.categories:
        threshold = all_thresholds.get(cat_score.category, default_threshold)
        exceeds = _severity_exceeds_threshold(cat_score.severity, threshold)

        decision = {
            "category": cat_score.category.value,
            "severity": cat_score.severity.value,
            "threshold": threshold.value,
            "blocked": exceeds,
        }
        category_decisions.append(decision)

        if exceeds:
            violations.append(decision)

    allow = len(violations) == 0

    return {
        "allow": allow,
        "violations": violations,
        "categories": category_decisions,
        "is_unsafe": result.is_unsafe,
        "blocklist_match": result.blocklist_match,
    }


def safety_threshold_json(
    text: str,
    thresholds: Optional[Dict[str, str]] = None,
    default_threshold: Optional[str] = None,
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Apply thresholds and return JSON result.

    Args:
        text: The user text to evaluate.
        thresholds: Dict of category name to severity threshold name.
        default_threshold: Default severity threshold string.
        categories: Optional list of category name strings.
        endpoint: Optional Azure endpoint override.
        api_key: Optional Azure API key override.

    Returns:
        JSON string of the threshold evaluation result.
    """
    import json

    # Convert string-based thresholds to enum-based
    category_map = {
        "Hate": SafetyCategory.HATE,
        "SelfHarm": SafetyCategory.SELF_HARM,
        "Sexual": SafetyCategory.SEXUAL,
        "Violence": SafetyCategory.VIOLENCE,
    }
    severity_map = {
        "Safe": SafetySeverity.SAFE,
        "Low": SafetySeverity.LOW,
        "Medium": SafetySeverity.MEDIUM,
        "High": SafetySeverity.HIGH,
    }

    enum_thresholds = None
    if thresholds:
        enum_thresholds = {}
        for cat_name, sev_name in thresholds.items():
            cat = category_map.get(cat_name)
            sev = severity_map.get(sev_name, SafetySeverity.LOW)
            if cat:
                enum_thresholds[cat] = sev

    default_sev = None
    if default_threshold:
        default_sev = severity_map.get(default_threshold, SafetySeverity.LOW)

    enum_categories = None
    if categories:
        enum_categories = [category_map.get(c, SafetyCategory.HATE) for c in categories]

    result = safety_threshold(
        text=text,
        thresholds=enum_thresholds,
        default_threshold=default_sev,
        categories=enum_categories,
        endpoint=endpoint,
        api_key=api_key,
    )
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else "This is a test message."
    print(safety_threshold_json(sample))
