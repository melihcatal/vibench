from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyCategoryScore:
    category: str
    score: float
    severity: Optional[int] = None
    flagged: bool = False


@dataclass
class SafetyResult:
    text: str
    categories: List[SafetyCategoryScore] = field(default_factory=list)
    blocklist_match: bool = False
    pii_detected: bool = False
    provider: str = "azure-ai-content-safety"
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @property
    def max_severity(self) -> int:
        severities = [c.severity for c in self.categories if c.severity is not None]
        return max(severities) if severities else 0

    @property
    def flagged(self) -> bool:
        return self.blocklist_match or any(c.flagged for c in self.categories)


def normalize_category(entry: Dict[str, Any]) -> SafetyCategoryScore:
    severity = entry.get("severity")
    category = str(entry.get("category", "unknown")).lower()
    return SafetyCategoryScore(
        category=category,
        score=float(severity if severity is not None else entry.get("score", 0.0)),
        severity=int(severity) if severity is not None else None,
        flagged=bool((severity or 0) >= 4 or entry.get("filtered", False)),
    )


def normalize_analysis_result(text: str, response_json: Dict[str, Any]) -> SafetyResult:
    categories = [normalize_category(item) for item in response_json.get("categoriesAnalysis", [])]
    return SafetyResult(
        text=text,
        categories=categories,
        blocklist_match=bool(response_json.get("blocklistsMatch")),
        pii_detected=bool(response_json.get("piiResult", {}).get("detected", False)),
        raw_response=response_json,
    )


def as_decision_dict(result: SafetyResult) -> Dict[str, Any]:
    return {
        "provider": result.provider,
        "text": result.text,
        "flagged": result.flagged,
        "blocklist_match": result.blocklist_match,
        "pii_detected": result.pii_detected,
        "max_severity": result.max_severity,
        "categories": [
            {
                "category": c.category,
                "score": c.score,
                "severity": c.severity,
                "flagged": c.flagged,
            }
            for c in result.categories
        ],
    }
