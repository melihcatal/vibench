"""
Moderate a batch of user messages and return per-message decisions.
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


def moderate_batch(
    texts: List[str],
    categories: Optional[List[SafetyCategory]] = None,
    output_type: str = "FourSeverityLevels",
    blocklist_names: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> List[SafetyResponse]:
    """
    Analyze a batch of text strings using Azure AI Content Safety
    and return a list of normalized SafetyResponse objects, one
    per input text.

    Each text is analyzed individually via the Azure SDK's
    analyze_text method. Results preserve ordering of the input list.

    Args:
        texts: List of user text strings to moderate.
        categories: Specific safety categories to check.
        output_type: Output format for severity.
        blocklist_names: Optional custom blocklist names.
        endpoint: Override Azure endpoint URL.
        key: Override Azure API key.

    Returns:
        List of SafetyResponse objects, one per input text.
    """
    client = create_content_safety_client(endpoint=endpoint, key=key)
    results: List[SafetyResponse] = []

    for text in texts:
        request = SafetyRequest(
            text=text,
            categories=categories,
            output_type=output_type,
            blocklist_names=blocklist_names,
        )
        azure_kwargs = build_azure_request(request)

        azure_response = client.analyze_text(
            text=azure_kwargs["text"],
            categories=azure_kwargs["categories"],
            output_type=azure_kwargs["output_type"],
            blocklist_names=azure_kwargs.get("blocklist_names"),
        )
        normalized = normalize_azure_response(azure_response, text)
        results.append(normalized)

    return results


def moderate_batch_dict(
    texts: List[str],
    categories: Optional[List[str]] = None,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> List[Dict]:
    """
    Convenience wrapper that returns a list of plain dicts.

    Args:
        texts: List of user text strings.
        categories: String names of categories.
        endpoint: Override Azure endpoint URL.
        key: Override Azure API key.

    Returns:
        List of dicts with moderation results per message.
    """
    cat_enums = None
    if categories:
        cat_enums = [SafetyCategory(c) for c in categories]

    responses = moderate_batch(
        texts,
        categories=cat_enums,
        endpoint=endpoint,
        key=key,
    )
    return [r.to_dict() for r in responses]
