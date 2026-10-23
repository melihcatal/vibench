from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class ModerationDecision:
    flagged: bool
    categories: Dict[str, float]


@dataclass
class RedactionResult:
    redacted_text: str
    spans: List[Dict[str, Any]]


def normalize_openai(result) -> ModerationDecision:
    categories = {k: v.score for k, v in result.category_scores.items()}
    return ModerationDecision(flagged=result.flagged, categories=categories)


def normalize_perspective(response: Dict) -> ModerationDecision:
    attrs = response.get("attributeScores", {})
    categories = {}
    for attr_name, attr_data in attrs.items():
        if "summaryScore" in attr_data:
            categories[attr_name.lower()] = attr_data["summaryScore"]["mean"]
    flagged = any(categories.get(cat, 0) > 0.5 for cat in categories)
    return ModerationDecision(flagged=flagged, categories=categories)
