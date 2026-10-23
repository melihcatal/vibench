"""
Local request, response, and normalization helpers for Text Content Safety.
Provider: Azure AI Content Safety
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class SafetyCategory(str, Enum):
    """Azure AI Content Safety categories."""
    HATE = "Hate"
    SELF_HARM = "SelfHarm"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"


class SeverityLevel(int, Enum):
    """Severity levels returned by Azure AI Content Safety."""
    SAFE = 0
    LOW = 2
    MEDIUM = 4
    HIGH = 6


@dataclass
class SafetyRequest:
    """Normalized request payload for text safety analysis."""
    text: str
    categories: Optional[List[SafetyCategory]] = None
    output_type: str = "FourSeverityLevels"
    halt_on_blocklist_hit: bool = False
    blocklist_names: Optional[List[str]] = None


@dataclass
class CategoryScore:
    """Per-category safety score."""
    category: str
    severity: int
    severity_label: str

    @property
    def is_unsafe(self) -> bool:
        return self.severity >= SeverityLevel.LOW


@dataclass
class SafetyResponse:
    """Normalized response from safety analysis."""
    text: str
    categories: List[CategoryScore] = field(default_factory=list)
    blocklist_result: Optional[Dict] = None
    overall_safe: bool = True

    @property
    def unsafe_categories(self) -> List[CategoryScore]:
        return [c for c in self.categories if c.is_unsafe]

    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "categories": [
                {
                    "category": c.category,
                    "severity": c.severity,
                    "severity_label": c.severity_label,
                    "is_unsafe": c.is_unsafe,
                }
                for c in self.categories
            ],
            "blocklist_result": self.blocklist_result,
            "overall_safe": self.overall_safe,
        }


SEVERITY_LABEL_MAP = {
    0: "Safe",
    2: "Low",
    4: "Medium",
    6: "High",
}


def normalize_azure_response(
    azure_response, text: str
) -> SafetyResponse:
    """
    Normalize the Azure AI Content Safety AnalyzeTextResult
    into a local SafetyResponse.

    Args:
        azure_response: Raw response object from Azure SDK.
        text: The original analyzed text.

    Returns:
        Normalized SafetyResponse.
    """
    categories = []
    overall_safe = True

    for cat in azure_response.categories_analysis:
        severity = cat.severity if cat.severity is not None else 0
        label = SEVERITY_LABEL_MAP.get(severity, "Unknown")
        cs = CategoryScore(
            category=str(cat.category),
            severity=severity,
            severity_label=label,
        )
        categories.append(cs)
        if cs.is_unsafe:
            overall_safe = False

    blocklist_result = None
    if hasattr(azure_response, 'blocklists_result') and azure_response.blocklists_result:
        blocklist_result = {
            "blocklist_name": azure_response.blocklists_result.blocklist_name,
            "blocklist_violation": azure_response.blocklists_result.blocklist_violation,
        }
        if blocklist_result.get("blocklist_violation"):
            overall_safe = False

    return SafetyResponse(
        text=text,
        categories=categories,
        blocklist_result=blocklist_result,
        overall_safe=overall_safe,
    )


def build_azure_request(request: SafetyRequest) -> Dict:
    """
    Build the Azure SDK kwargs from a normalized SafetyRequest.

    Args:
        request: Normalized safety request.

    Returns:
        Dict suitable for Azure Content Safety analyze_text options.
    """
    categories = request.categories or [
        SafetyCategory.HATE,
        SafetyCategory.SELF_HARM,
        SafetyCategory.SEXUAL,
        SafetyCategory.VIOLENCE,
    ]

    return {
        "text": request.text,
        "categories": categories,
        "output_type": request.output_type,
        "halt_on_blocklist_hit": request.halt_on_blocklist_hit,
        "blocklist_names": request.blocklist_names,
    }
