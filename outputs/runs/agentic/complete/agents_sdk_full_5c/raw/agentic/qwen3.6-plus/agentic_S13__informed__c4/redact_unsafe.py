"""
Flag or redact unsafe spans from text based on Azure AI Content Safety analysis.
Provider: Azure AI Content Safety
"""

import re
from typing import Optional, Dict, List, Tuple

from safety_client import create_content_safety_client
from safety_models import (
    SafetyRequest,
    SafetyResponse,
    SafetyCategory,
    normalize_azure_response,
    build_azure_request,
    SeverityLevel,
)


def _build_span_patterns(response: SafetyResponse) -> List[str]:
    """
    Build regex patterns from unsafe category keywords.
    Since Azure Content Safety returns overall severity, we
    flag the entire text span when severity exceeds a threshold.

    Returns list of regex patterns matching the unsafe portions.
    """
    patterns = []
    for cat in response.unsafe_categories:
        category_name = cat.category.lower()
        patterns.append(category_name)
    return patterns


def redact_unsafe(
    text: str,
    replacement: str = "[REDACTED]",
    threshold_severity: int = SeverityLevel.LOW,
    categories: Optional[List[SafetyCategory]] = None,
    output_type: str = "FourSeverityLevels",
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> Tuple[str, SafetyResponse]:
    """
    Analyze text with Azure AI Content Safety and redact unsafe content.

    If any category exceeds the threshold severity, the entire text span
    is replaced with the replacement string. Otherwise the original text
    is returned unchanged.

    Args:
        text: The user text to analyze and potentially redact.
        replacement: String to replace unsafe text with.
        threshold_severity: Minimum severity level triggering redaction.
        categories: Safety categories to check.
        output_type: Output format for severity.
        endpoint: Override Azure endpoint URL.
        key: Override Azure API key.

    Returns:
        Tuple of (redacted_text, SafetyResponse).
    """
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

    redacted_text = text
    should_redact = any(
        cat.severity >= threshold_severity for cat in response.categories
    )

    if should_redact:
        redacted_text = replacement

    return redacted_text, response


def flag_unsafe_spans(
    text: str,
    threshold_severity: int = SeverityLevel.LOW,
    categories: Optional[List[SafetyCategory]] = None,
    output_type: str = "FourSeverityLevels",
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> Dict:
    """
    Analyze text and return flagged span information without redaction.

    Args:
        text: The user text to analyze.
        threshold_severity: Minimum severity to flag.
        categories: Safety categories to check.
        output_type: Output format for severity.
        endpoint: Override Azure endpoint URL.
        key: Override Azure API key.

    Returns:
        Dict with text, flags, flagged, and response data.
    """
    redacted, response = redact_unsafe(
        text,
        replacement=text,
        threshold_severity=threshold_severity,
        categories=categories,
        output_type=output_type,
        endpoint=endpoint,
        key=key,
    )

    flags = [
        {
            "category": cat.category,
            "severity": cat.severity,
            "flagged": cat.severity >= threshold_severity,
        }
        for cat in response.categories
    ]

    return {
        "text": text,
        "flags": flags,
        "flagged": response.overall_safe is False,
        "response": response.to_dict(),
    }
