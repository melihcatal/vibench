"""
Local helper: Define local request, response, and normalization helpers
for Text Content Safety.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SafetyRequest:
    """Normalized request payload for a single text moderation call."""
    text: str
    categories: list[str] = field(default_factory=lambda: ["Hate", "SelfHarm", "Sexual", "Violence"])
    halt_on_block: bool = False


@dataclass
class CategoryScore:
    """Score result for a single safety category."""
    category: str
    severity: int  # 0-7 for Azure AI Content Safety
    blocked: bool = False


@dataclass
class SafetyResponse:
    """Normalized response from a moderation call."""
    request_id: str
    categories: list[CategoryScore]
    overall_blocked: bool = False
    raw_severities: dict[str, int] = field(default_factory=dict)
    moderation_action: str = "allow"


def normalize_category_name(azure_category: str) -> str:
    """Map Azure AI Content Safety category to a normalized string."""
    mapping = {
        "Hate": "hate",
        "SelfHarm": "self_harm",
        "Sexual": "sexual",
        "Violence": "violence",
    }
    return mapping.get(azure_category, azure_category.lower())


def build_moderation_action(
    categories: list[CategoryScore],
    blocked: bool,
) -> str:
    """Determine the moderation action based on category scores."""
    if blocked:
        return "block"
    max_severity = max((c.severity for c in categories), default=0)
    if max_severity >= 5:
        return "review"
    return "allow"


def parse_raw_response(
    response_data: dict,
) -> SafetyResponse:
    """Parse raw Azure AI Content Safety API response into normalized form."""
    categories = []
    raw_severities = {}
    overall_blocked = False

    analysis_result = response_data.get("blocklistsMatch", [])
    if analysis_result:
        overall_blocked = True

    for cat_data in response_data.get("categoriesAnalysis", []):
        cat_name = cat_data.get("category", "Unknown")
        severity = cat_data.get("severity", 0)
        raw_severities[normalize_category_name(cat_name)] = severity
        categories.append(
            CategoryScore(
                category=normalize_category_name(cat_name),
                severity=severity,
            )
        )

    return SafetyResponse(
        request_id=response_data.get("id", ""),
        categories=categories,
        overall_blocked=overall_blocked,
        raw_severities=raw_severities,
        moderation_action=build_moderation_action(categories, overall_blocked),
    )


def format_for_api(text: str, categories: list[str], output_type: str = "EightSeverityLevels") -> dict:
    """Format a request for the Azure AI Content Safety analyzeText API."""
    return {
        "text": text,
        "categories": categories,
        "outputType": output_type,
    }
