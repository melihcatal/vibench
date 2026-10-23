"""
safety_threshold.py - Applies category thresholds to decide whether to allow text.

Provider: Azure AI Content Safety
  - SDK: azure-ai-contentsafety
  - Env: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
  - Endpoint: .cognitiveservices.azure.com
  - Categories: Hate, SelfHarm, Sexual, Violence
"""

from __future__ import annotations

from typing import Optional, List, Dict, Any

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from safety_client import create_content_safety_client
from safety_models import (
    ModerationResponse,
    normalize_azure_response,
    apply_thresholds,
    AZURE_CATEGORIES,
)

CATEGORY_MAP = {
    "Hate": TextCategory.HATE,
    "SelfHarm": TextCategory.SELF_HARM,
    "Sexual": TextCategory.SEXUAL,
    "Violence": TextCategory.VIOLENCE,
}

DEFAULT_THRESHOLDS: Dict[str, int] = {
    "Hate": 0,
    "SelfHarm": 0,
    "Sexual": 0,
    "Violence": 0,
}


class ThresholdDecision:
    """Holds the result of a threshold-based moderation decision."""

    def __init__(
        self,
        text: str,
        allowed: bool,
        moderation_response: ModerationResponse,
        threshold_results: Dict[str, bool],
        thresholds_applied: Dict[str, int],
    ):
        self.text = text
        self.allowed = allowed
        self.moderation_response = moderation_response
        self.threshold_results = threshold_results
        self.thresholds_applied = thresholds_applied

    @property
    def blocked_categories(self) -> List[str]:
        """Return list of categories that failed the threshold check."""
        return [cat for cat, passed in self.threshold_results.items() if not passed]

    @property
    def blocking_reason(self) -> str:
        """Human-readable reason for blocking, if applicable."""
        if self.allowed:
            return "Text passed all category thresholds."
        blocked = self.blocked_categories
        return f"Text blocked due to: {', '.join(blocked)}"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the decision to a dictionary."""
        return {
            "text": self.text,
            "allowed": self.allowed,
            "blocked_categories": self.blocked_categories,
            "blocking_reason": self.blocking_reason,
            "threshold_results": self.threshold_results,
            "thresholds_applied": self.thresholds_applied,
            "moderation_severity": {
                c.category: c.severity for c in self.moderation_response.categories
            },
        }


def apply_safety_threshold(
    text: str,
    thresholds: Optional[Dict[str, int]] = None,
    categories: Optional[List[str]] = None,
    client: Optional[ContentSafetyClient] = None,
) -> ThresholdDecision:
    """
    Apply per-category severity thresholds to decide whether to allow text.

    Azure AI Content Safety returns severity values of 0 (safe), 2 (low),
    4 (medium), and 6 (high). This function compares each category's
    severity against the configured threshold.

    Args:
        text: The input text to evaluate.
        thresholds: Dict mapping category name to maximum allowed severity.
                    Defaults to DEFAULT_THRESHOLDS (allow only safe content).
        categories: Categories to check. Defaults to all Azure categories.
        client: Optional pre-configured ContentSafetyClient.

    Returns:
        ThresholdDecision indicating whether the text is allowed.

    Example:
        # Allow low-severity content but block medium and above
        thresholds = {"Hate": 2, "SelfHarm": 0, "Sexual": 2, "Violence": 2}
        decision = apply_safety_threshold(text, thresholds=thresholds)
    """
    if not text or not text.strip():
        return ThresholdDecision(
            text=text,
            allowed=True,
            moderation_response=ModerationResponse(text=text, overall_safe=True),
            threshold_results={},
            thresholds_applied=thresholds or DEFAULT_THRESHOLDS,
        )

    if client is None:
        client = create_content_safety_client()

    if thresholds is None:
        thresholds = dict(DEFAULT_THRESHOLDS)

    if categories is None:
        categories = AZURE_CATEGORIES

    text_categories = [CATEGORY_MAP[c] for c in categories if c in CATEGORY_MAP]

    options = AnalyzeTextOptions(
        text=text,
        categories=text_categories,
        output_type=0,
    )

    azure_response = client.analyze_text(options)
    moderation_response = normalize_azure_response(text=text, azure_response=azure_response)

    threshold_results = apply_thresholds(moderation_response, thresholds)

    allowed = all(threshold_results.values())

    return ThresholdDecision(
        text=text,
        allowed=allowed,
        moderation_response=moderation_response,
        threshold_results=threshold_results,
        thresholds_applied=thresholds,
    )


def apply_safety_threshold_batch(
    texts: List[str],
    thresholds: Optional[Dict[str, int]] = None,
    categories: Optional[List[str]] = None,
    client: Optional[ContentSafetyClient] = None,
) -> List[ThresholdDecision]:
    """
    Apply thresholds to a batch of texts.

    Args:
        texts: List of texts to evaluate.
        thresholds: Per-category severity thresholds.
        categories: Categories to check.
        client: Optional pre-configured ContentSafetyClient.

    Returns:
        List of ThresholdDecision objects, one per input text.
    """
    return [
        apply_safety_threshold(text, thresholds=thresholds, categories=categories, client=client)
        for text in texts
    ]


def get_tiered_thresholds(tier: str) -> Dict[str, int]:
    """
    Return predefined threshold sets for common moderation tiers.

    Tiers:
        - "strict": Block any content with severity > 0 (default)
        - "moderate": Allow low severity (<=2), block medium and above
        - "lenient": Allow medium severity (<=4), block only high

    Args:
        tier: The moderation tier name.

    Returns:
        Dict of category-to-threshold mappings.
    """
    tiers = {
        "strict": {"Hate": 0, "SelfHarm": 0, "Sexual": 0, "Violence": 0},
        "moderate": {"Hate": 2, "SelfHarm": 2, "Sexual": 2, "Violence": 2},
        "lenient": {"Hate": 4, "SelfHarm": 4, "Sexual": 4, "Violence": 4},
    }
    return tiers.get(tier, dict(DEFAULT_THRESHOLDS))
