"""
safety_models.py - Define local request, response, and normalization helpers for Text Content Safety.

Works with Azure AI Content Safety responses and normalizes them into
a consistent internal format for downstream processing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# Azure Content Safety category identifiers
AZURE_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]

SEVERITY_MAP = {
    0: "safe",
    2: "low",
    4: "medium",
    6: "high",
}


@dataclass
class ModerationRequest:
    """Internal representation of a text moderation request."""
    text: str
    blocklist_names: Optional[List[str]] = None
    halt_on_blocklist_match: bool = False
    categories: Optional[List[str]] = None


@dataclass
class CategoryScore:
    """Normalized score for a single safety category."""
    category: str
    severity: int
    label: str
    details: Optional[str] = None


@dataclass
class ModerationResponse:
    """Normalized moderation response for a single text item."""
    text: str
    categories: List[CategoryScore] = field(default_factory=list)
    blocklist_match: bool = False
    blocklist_name: Optional[str] = None
    overall_safe: bool = True
    raw_response: Optional[Dict[str, Any]] = None

    @property
    def unsafe_categories(self) -> List[CategoryScore]:
        """Return categories that are not safe (severity > 0)."""
        return [c for c in self.categories if c.severity > 0]


@dataclass
class BatchModerationResponse:
    """Container for batch moderation results."""
    results: List[ModerationResponse] = field(default_factory=list)

    @property
    def total_items(self) -> int:
        return len(self.results)

    @property
    def unsafe_count(self) -> int:
        return sum(1 for r in self.results if not r.overall_safe)


@dataclass
class RedactionResult:
    """Result of redacting unsafe content from text."""
    original_text: str
    redacted_text: str
    flagged_spans: List[Dict[str, Any]] = field(default_factory=list)
    was_modified: bool = False


def normalize_azure_response(
    text: str,
    azure_response: Any,
    blocklist_match: bool = False,
    blocklist_name: Optional[str] = None,
) -> ModerationResponse:
    """
    Normalize an Azure AI Content Safety SDK response into a ModerationResponse.

    Args:
        text: The original input text.
        azure_response: The raw response object from Azure Content Safety SDK.
        blocklist_match: Whether a custom blocklist matched.
        blocklist_name: Name of the matched blocklist, if any.

    Returns:
        A normalized ModerationResponse.
    """
    categories = []
    overall_safe = True
    raw = {}

    if azure_response is not None:
        raw = _response_to_dict(azure_response)

        text_categories = getattr(azure_response, "categories_analysis", [])
        for cat_result in text_categories:
            cat_name = getattr(cat_result, "category", "Unknown")
            severity = getattr(cat_result, "severity", 0)
            label = SEVERITY_MAP.get(severity, "unknown")
            categories.append(CategoryScore(
                category=cat_name,
                severity=severity,
                label=label,
            ))
            if severity > 0:
                overall_safe = False

    return ModerationResponse(
        text=text,
        categories=categories,
        blocklist_match=blocklist_match,
        blocklist_name=blocklist_name,
        overall_safe=overall_safe and not blocklist_match,
        raw_response=raw,
    )


def _response_to_dict(response: Any) -> Dict[str, Any]:
    """Convert an Azure SDK response object to a plain dict."""
    if response is None:
        return {}
    if hasattr(response, "as_dict"):
        return response.as_dict()
    if hasattr(response, "__dict__"):
        return response.__dict__
    return {"raw": str(response)}


def extract_unsafe_spans(
    text: str,
    categories: List[CategoryScore],
    redact_token: str = "[REDACTED]",
) -> RedactionResult:
    """
    Produce a redaction result by replacing the full text if any category is unsafe.

    For more precise span-level redaction, callers should use NLP-based span
    detection; this helper provides a conservative full-text replacement
    when unsafe content is detected.
    """
    flagged_spans = []
    was_modified = False

    unsafe_cats = [c for c in categories if c.severity > 0]
    if unsafe_cats:
        was_modified = True
        for cat in unsafe_cats:
            flagged_spans.append({
                "category": cat.category,
                "severity": cat.severity,
                "span": (0, len(text)),
                "redacted_value": redact_token,
            })

    redacted_text = redact_token if was_modified else text

    return RedactionResult(
        original_text=text,
        redacted_text=redacted_text,
        flagged_spans=flagged_spans,
        was_modified=was_modified,
    )


def apply_thresholds(
    response: ModerationResponse,
    thresholds: Optional[Dict[str, int]] = None,
) -> Dict[str, bool]:
    """
    Apply per-category severity thresholds to decide whether to allow each category.

    Args:
        response: A ModerationResponse with category scores.
        thresholds: Dict mapping category name to maximum allowed severity.
                    Defaults to requiring severity 0 for all categories.

    Returns:
        Dict mapping category name to a boolean indicating whether it passes the threshold.
    """
    if thresholds is None:
        thresholds = {cat: 0 for cat in AZURE_CATEGORIES}

    results = {}
    for cat_score in response.categories:
        threshold = thresholds.get(cat_score.category, 0)
        results[cat_score.category] = cat_score.severity <= threshold

    return results
