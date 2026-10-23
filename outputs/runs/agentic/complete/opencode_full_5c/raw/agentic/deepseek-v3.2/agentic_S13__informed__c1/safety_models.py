from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "Hate"
    VIOLENCE = "Violence"
    SEXUAL = "Sexual"
    SELF_HARM = "SelfHarm"


@dataclass
class SafetyThresholds:
    """
    Define local request, response, and normalization helpers for Text Content Safety.
    Thresholds for different safety categories (0-4 severity scale).
    """

    hate: int = 2  # Medium severity
    violence: int = 2
    sexual: int = 2
    self_harm: int = 1  # Lower threshold for self-harm

    def to_dict(self) -> Dict[str, int]:
        return {
            "hate": self.hate,
            "violence": self.violence,
            "sexual": self.sexual,
            "self_harm": self.self_harm,
        }


@dataclass
class ModerationRequest:
    text: str
    categories: Optional[List[SafetyCategory]] = None
    return_span_info: bool = False

    def to_azure_format(self) -> Dict[str, Any]:
        """Convert to Azure Content Safety format"""
        return {
            "text": self.text,
            "categories": [
                cat.value for cat in (self.categories or list(SafetyCategory))
            ],
            "outputType": "FourSeverityLevels",
        }


@dataclass
class ModerationResult:
    text: str
    safe: bool
    category_scores: Dict[str, int]
    severity: int
    decision: str

    @classmethod
    def from_azure_response(cls, text: str, response: Any) -> "ModerationResult":
        """Create from Azure Content Safety response"""
        category_scores = {}
        max_severity = 0
        safe = True

        if hasattr(response, "categories_analysis"):
            for cat_analysis in response.categories_analysis:
                category = cat_analysis.category.value
                severity = (
                    cat_analysis.severity if hasattr(cat_analysis, "severity") else 0
                )
                category_scores[category] = severity

                if severity > max_severity:
                    max_severity = severity

                if severity >= 2:
                    safe = False

        decision = "allow" if safe else "block"

        return cls(
            text=text,
            safe=safe,
            category_scores=category_scores,
            severity=max_severity,
            decision=decision,
        )


def normalize_severity(severity: int) -> str:
    """Normalize severity score to human-readable level"""
    if severity == 0:
        return "safe"
    elif severity == 1:
        return "low"
    elif severity == 2:
        return "medium"
    elif severity == 3:
        return "high"
    else:
        return "very_high"
