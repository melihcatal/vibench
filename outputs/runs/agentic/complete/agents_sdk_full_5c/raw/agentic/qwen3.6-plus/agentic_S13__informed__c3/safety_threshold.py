"""
Apply category thresholds to decide whether to allow text using Azure AI Content Safety.

Provider: Azure AI Content Safety
Endpoint: {azure_endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from moderate_text import moderate_text
from safety_models import ModerationResponse


@dataclass
class CategoryThreshold:
    """Maximum allowed severity score for a single category."""

    category: str
    max_severity: int = 3  # Azure uses 0-7


@dataclass
class ThresholdDecision:
    """Result of threshold evaluation against a moderation response."""

    text: str
    allowed: bool = True
    violations: List[str] = field(default_factory=list)
    moderation: Optional[ModerationResponse] = None


def apply_thresholds(
    text: str,
    thresholds: Optional[List[CategoryThreshold]] = None,
    config: Optional[Dict[str, str]] = None,
) -> ThresholdDecision:
    """
    Analyse *text* with Azure AI Content Safety and check each category
    against *thresholds*.  Return a ThresholdDecision indicating whether
    the text is allowed.

    Provider: Azure AI Content Safety
    """
    moderation = moderate_text(text, config=config)

    if thresholds is None:
        thresholds = [CategoryThreshold(cat=c) for c in moderation.categories]

    violations: List[str] = []
    for cat_result in moderation.categories:
        threshold_obj = next(
            (t for t in thresholds if t.category == cat_result.category),
            None,
        )
        if threshold_obj is None:
            continue
        if cat_result.severity > threshold_obj.max_severity:
            violations.append(
                f"{cat_result.category}: severity {cat_result.severity} "
                f"exceeds threshold {threshold_obj.max_severity}"
            )

    return ThresholdDecision(
        text=text,
        allowed=len(violations) == 0,
        violations=violations,
        moderation=moderation,
    )


if __name__ == "__main__":
    sample = "This message might be slightly problematic."
    decision = apply_thresholds(sample)
    print(f"Allowed: {decision.allowed}")
    if not decision.allowed:
        for v in decision.violations:
            print(f"  Violation: {v}")
