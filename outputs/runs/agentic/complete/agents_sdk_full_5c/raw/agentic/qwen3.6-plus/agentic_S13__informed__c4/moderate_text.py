"""
Moderate a single user text for unsafe or policy-violating content.
Provider: Azure AI Content Safety
"""

from typing import Optional, Dict, List

from safety_client import create_content_safety_client
from safety_models import (
    SafetyRequest,
    SafetyResponse,
    SafetyCategory,
    normalize_azure_response,
    build_azure_request,
)


def moderate_text(
    text: str,
    categories: Optional[List[SafetyCategory]] = None,
    output_type: str = "FourSeverityLevels",
    blocklist_names: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> SafetyResponse:
    """
    Analyze a single text string using Azure AI Content Safety
    and return a normalized SafetyResponse with per-category
    severity scores and an overall safety decision.

    Args:
        text: The user text to moderate.
        categories: Specific safety categories to check.
            Defaults to all four Azure categories.
        output_type: Output format for severity. Defaults to
            'FourSeverityLevels' (0, 2, 4, 6).
        blocklist_names: Optional custom blocklist names to apply.
        endpoint: Override Azure endpoint URL.
        key: Override Azure API key.

    Returns:
        SafetyResponse with category scores and overall safety flag.
    """
    request = SafetyRequest(
        text=text,
        categories=categories,
        output_type=output_type,
        blocklist_names=blocklist_names,
    )

    client = create_content_safety_client(endpoint=endpoint, key=key)
    azure_kwargs = build_azure_request(request)

    azure_response = client.analyze_text(
        text=azure_kwargs["text"],
        categories=azure_kwargs["categories"],
        output_type=azure_kwargs["output_type"],
        blocklist_names=azure_kwargs.get("blocklist_names"),
    )

    return normalize_azure_response(azure_response, text)


def moderate_text_dict(
    text: str,
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> Dict:
    """
    Convenience wrapper that returns a plain dict instead of SafetyResponse.

    Args:
        text: The user text to moderate.
        categories: String names of categories (e.g. ['Hate', 'Sexual']).
        endpoint: Override Azure endpoint URL.
        key: Override Azure API key.

    Returns:
        Dict with moderation results.
    """
    cat_enums = None
    if categories:
        cat_enums = [SafetyCategory(c) for c in categories]

    response = moderate_text(text, categories=cat_enums, endpoint=endpoint, key=key)
    return response.to_dict()
