"""
Define local request, response, and normalization helpers for Text Content Safety
using Azure AI Content Safety response schemas.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# Azure AI Content Safety category names
AZURE_CATEGORIES = ["Hate", "SelfHarm", "Sexual", "Violence"]

# Map Azure severity levels (0-7) to a normalised 0.0-1.0 score
_SEVERITY_TO_SCORE = {
    0: 0.0,
    1: 0.0,
    2: 0.143,
    3: 0.286,
    4: 0.429,
    5: 0.571,
    6: 0.714,
    7: 0.857,
}


@dataclass
class CategoryResult:
    """Normalized result for one safety category from Azure AI Content Safety."""

    category: str
    severity: int = 0
    score: float = 0.0
    is_flagged: bool = False


@dataclass
class ModerationResponse:
    """Normalized moderation response wrapping Azure AI Content Safety results."""

    text: str
    categories: List[CategoryResult] = field(default_factory=list)
    max_severity: int = 0
    is_safe: bool = True
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class BatchModerationResult:
    """Result for one item within a batch moderation response."""

    index: int
    text: str
    moderation: ModerationResponse


@dataclass
class BatchModerationResponse:
    """Aggregated response for a batch of texts."""

    results: List[BatchModerationResult] = field(default_factory=list)


@dataclass
class RedactionResult:
    """Result after redacting unsafe spans from text."""

    original: str
    redacted: str
    flagged_spans: List[Dict[str, Any]] = field(default_factory=list)


def normalize_severity(severity: int) -> float:
    """Convert Azure severity (0-7) to a 0.0-1.0 score."""
    return _SEVERITY_TO_SCORE.get(severity, 0.0)


def parse_azure_analyze_response(
    text: str, raw: Dict[str, Any]
) -> ModerationResponse:
    """Parse the Azure AI Content Safety /text:analyze JSON response."""
    categories: List[CategoryResult] = []
    max_sev = 0
    is_safe = True

    cat_results = raw.get("categoriesAnalysis", [])
    for entry in cat_results:
        cat_name = entry.get("category", "")
        sev = entry.get("severity", 0)
        score = normalize_severity(sev)
        flagged = sev >= 4
        categories.append(
            CategoryResult(
                category=cat_name, severity=sev, score=score, is_flagged=flagged
            )
        )
        if sev > max_sev:
            max_sev = sev
        if flagged:
            is_safe = False

    return ModerationResponse(
        text=text,
        categories=categories,
        max_severity=max_sev,
        is_safe=is_safe,
        raw_response=raw,
    )


def build_redaction_spans(
    moderation: ModerationResponse,
) -> List[Dict[str, Any]]:
    """Derive span-level redaction markers from a ModerationResponse."""
    spans = []
    for cat in moderation.categories:
        if cat.is_flagged:
            spans.append(
                {
                    "category": cat.category,
                    "severity": cat.severity,
                    "score": cat.score,
                    "label": f"[{cat.category.upper()}]",
                }
            )
    return spans
