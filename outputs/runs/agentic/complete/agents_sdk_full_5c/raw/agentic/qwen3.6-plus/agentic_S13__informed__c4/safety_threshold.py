"""
Apply category thresholds to decide whether to allow text.
Provider: Azure AI Content Safety
"""

from typing import Optional, Dict, List, Tuple

from safety_client import create_content_safety_client
from safety_models import (
    SafetyRequest,
    SafetyResponse,
    SafetyCategory,
    CategoryScore,
    normalize_azure_response,
    build_azure_request,
    SeverityLevel,
)

DEFAULT_THRESHOLDS = {
    SafetyCategory.HATE: SeverityLevel.MEDIUM,
    SafetyCategory.SELF_HARM: SeverityLevel.LOW,
    SafetyCategory.SEXUAL: SeverityLevel.MEDIUM,
    SafetyCategory.VIOLENCE: SeverityLevel.MEDIUM,
}


def apply_thresholds(
    text: str,
    thresholds: Optional[Dict[SafetyCategory, int]] = None,
    categories: Optional[List[SafetyCategory]] = None,
    output_type: str = "FourSeverityLevels",
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> Tuple[bool, Dict[str, bool], SafetyResponse]:
    """
    Analyze text with Azure AI Content Safety and apply per-category
    severity thresholds to determine whether the text should be allowed.

    Each category has its own threshold. A category is considered blocked
    when its severity meets or exceeds its threshold. The text is allowed
    only if no category exceeds its threshold.

    Args:
        text: The user text to evaluate.
        thresholds: Mapping of SafetyCategory to minimum blocking severity.
            Uses DEFAULT_THRESHOLDS when not provided.
        categories: Safety categories to check.
        output_type: Output format for severity.
        endpoint: Override Azure endpoint URL.
        key: Override Azure API key.

    Returns:
        Tuple of (allowed, per_category_decisions, SafetyResponse).
    """
    if thresholds is None:
        thresholds = dict(DEFAULT_THRESHOLDS)

    request = SafetyRequest(
        text=text,
        categories=categories,
        output_type=output_type,
    )

    client = create_content_safety_client(endpoint=endpoint, key=key)
    azure_kwargs = build_azure_request(request)

    azure_response = client.analyze_text(
        text=azure_kwargs["text"],
        categories=azure_kwargs["categories"],
        output_type=azure_kwargs["output_type"],
    )

    response = normalize_azure_response(azure_response, text)

    category_decisions: Dict[str, bool] = {}
    allowed = True

    for cat_score in response.categories:
        threshold = thresholds.get(
            SafetyCategory(cat_score.category), SeverityLevel.HIGH
        )
        blocked = cat_score.severity >= threshold
        category_decisions[cat_score.category] = blocked
        if blocked:
            allowed = False

    return allowed, category_decisions, response


def evaluate_with_thresholds_dict(
    text: str,
    thresholds: Optional[Dict[str, int]] = None,
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> Dict:
    """
    Convenience wrapper returning a plain dict result.

    Args:
        text: The user text to evaluate.
        thresholds: Mapping of category name strings to severity integers.
        categories: String names of categories.
        endpoint: Override Azure endpoint URL.
        key: Override Azure API key.

    Returns:
        Dict with allowed flag, per-category decisions, and response data.
    """
    cat_enums = None
    if categories:
        cat_enums = [SafetyCategory(c) for c in categories]

    threshold_enums = None
    if thresholds:
        threshold_enums = {SafetyCategory(k): v for k, v in thresholds.items()}

    allowed, decisions, response = apply_thresholds(
        text,
        thresholds=threshold_enums,
        categories=cat_enums,
        endpoint=endpoint,
        key=key,
    )

    return {
        "allowed": allowed,
        "category_decisions": decisions,
        "response": response.to_dict(),
    }
