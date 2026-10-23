"""
Local request, response, and normalization helpers for Text Content Safety.
Provider-agnostic data models for working with Azure AI Content Safety results.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import json


class SafetyCategory(str, Enum):
    """Categories used by Azure AI Content Safety."""
    HATE = "Hate"
    SELF_HARM = "SelfHarm"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"


class SafetySeverity(str, Enum):
    """Severity levels for content safety scores."""
    SAFE = "Safe"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class SafetyRequest:
    """Normalized request for text moderation."""
    text: str
    categories: Optional[List[SafetyCategory]] = None
    blocklist_names: Optional[List[str]] = None
    halt_on_blocklist_item: bool = False
    output_type: str = "FourSeverityLevels"

    def to_azure_options(self):
        """Convert to Azure AI Content Safety AnalyzeTextOptions."""
        from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

        category_map = {
            SafetyCategory.HATE: TextCategory.HATE,
            SafetyCategory.SELF_HARM: TextCategory.SELF_HARM,
            SafetyCategory.SEXUAL: TextCategory.SEXUAL,
            SafetyCategory.VIOLENCE: TextCategory.VIOLENCE,
        }

        azure_categories = []
        if self.categories:
            for cat in self.categories:
                if cat in category_map:
                    azure_categories.append(category_map[cat])
        else:
            azure_categories = list(category_map.values())

        return AnalyzeTextOptions(
            text=self.text,
            categories=azure_categories,
            output_type=self.output_type,
        )


@dataclass
class CategoryScore:
    """Score result for a single safety category."""
    category: SafetyCategory
    severity: SafetySeverity
    score: int = 0


@dataclass
class SafetyResponse:
    """Normalized response from text moderation."""
    is_unsafe: bool
    categories: List[CategoryScore] = field(default_factory=list)
    blocklist_match: Optional[str] = None
    raw_response: Optional[dict] = None

    @property
    def max_severity(self) -> SafetySeverity:
        """Return the highest severity level found."""
        severity_order = [
            SafetySeverity.SAFE,
            SafetySeverity.LOW,
            SafetySeverity.MEDIUM,
            SafetySeverity.HIGH,
        ]
        max_sev = SafetySeverity.SAFE
        for cat in self.categories:
            if severity_order.index(cat.severity) > severity_order.index(max_sev):
                max_sev = cat.severity
        return max_sev

    @property
    def flagged_categories(self) -> List[SafetyCategory]:
        """Return list of categories that are not safe."""
        return [c.category for c in self.categories if c.severity != SafetySeverity.SAFE]

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "is_unsafe": self.is_unsafe,
            "categories": [
                {
                    "category": c.category.value,
                    "severity": c.severity.value,
                    "score": c.score,
                }
                for c in self.categories
            ],
            "blocklist_match": self.blocklist_match,
            "max_severity": self.max_severity.value,
        }


@dataclass
class BatchModerationResult:
    """Result for a batch of moderation requests."""
    results: List[SafetyResponse] = field(default_factory=list)
    total_count: int = 0
    unsafe_count: int = 0

    @property
    def unsafe_rate(self) -> float:
        """Calculate the rate of unsafe content in the batch."""
        if self.total_count == 0:
            return 0.0
        return self.unsafe_count / self.total_count

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "total_count": self.total_count,
            "unsafe_count": self.unsafe_count,
            "unsafe_rate": round(self.unsafe_rate, 4),
            "results": [r.to_dict() for r in self.results],
        }


def parse_azure_response(raw_response) -> SafetyResponse:
    """Parse an Azure AI Content Safety response into normalized SafetyResponse."""
    severity_map = {0: SafetySeverity.SAFE, 2: SafetySeverity.LOW, 4: SafetySeverity.MEDIUM, 6: SafetySeverity.HIGH}
    category_map = {
        "Hate": SafetyCategory.HATE,
        "SelfHarm": SafetyCategory.SELF_HARM,
        "Sexual": SafetyCategory.SEXUAL,
        "Violence": SafetyCategory.VIOLENCE,
    }

    categories = []
    is_unsafe = False

    if raw_response.categories_analysis:
        for cat_result in raw_response.categories_analysis:
            cat_name = str(cat_result.category).split(".")[-1]
            severity_val = getattr(cat_result, "severity", 0)

            safety_cat = category_map.get(cat_name, SafetyCategory.HATE)
            safety_sev = severity_map.get(severity_val, SafetySeverity.SAFE)

            if safety_sev != SafetySeverity.SAFE:
                is_unsafe = True

            categories.append(CategoryScore(
                category=safety_cat,
                severity=safety_sev,
                score=severity_val,
            ))

    blocklist_match = None
    if hasattr(raw_response, "blocklists_result") and raw_response.blocklists_result:
        if raw_response.blocklists_result.blocklist_name:
            blocklist_match = raw_response.blocklists_result.blocklist_name

    return SafetyResponse(
        is_unsafe=is_unsafe,
        categories=categories,
        blocklist_match=blocklist_match,
        raw_response={"categories_analysis": str(raw_response.categories_analysis)},
    )


def parse_batch_azure_response(raw_response) -> SafetyResponse:
    """Parse Azure batch moderation response into normalized SafetyResponse."""
    return parse_azure_response(raw_response)


def serialize_response(response: SafetyResponse) -> str:
    """Serialize a SafetyResponse to JSON string."""
    return json.dumps(response.to_dict(), indent=2)
