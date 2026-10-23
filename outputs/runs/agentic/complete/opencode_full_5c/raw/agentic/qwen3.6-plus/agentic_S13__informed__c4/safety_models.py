from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModerationRequest:
    text: str
    categories: list[str] | None = None
    output_type: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CategoryScore:
    category: str
    severity: str
    severity_value: int
    flagged: bool = False


@dataclass
class ModerationResult:
    text: str
    categories: list[CategoryScore]
    highest_severity: int
    overall_flagged: bool
    blocklist_matches: list[dict[str, str]] = field(default_factory=list)
    raw_response: dict | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationRequest:
    messages: list[ModerationRequest]


@dataclass
class BatchModerationResult:
    results: list[ModerationResult]
    total_flagged: int
    total_safe: int

    @property
    def summary(self) -> dict:
        return {
            "total": len(self.results),
            "flagged": self.total_flagged,
            "safe": self.total_safe,
        }


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    flagged_spans: list[dict[str, Any]]
    categories_triggered: list[str]


@dataclass
class ThresholdResult:
    text: str
    allowed: bool
    category_decisions: dict[str, dict[str, Any]]
    reason: str


def build_category_score(
    category_name: str,
    severity_label: str,
    severity_value: int,
    threshold_map: dict[str, int] | None = None,
) -> CategoryScore:
    threshold = threshold_map.get(category_name, 1) if threshold_map else 1
    flagged = severity_value >= threshold
    return CategoryScore(
        category=category_name,
        severity=severity_label,
        severity_value=severity_value,
        flagged=flagged,
    )


def moderation_result_from_parsed(
    text: str,
    parsed: dict,
    raw_response: dict | None = None,
    threshold_map: dict[str, int] | None = None,
) -> ModerationResult:
    categories = []
    any_flagged = False
    for cat_name, cat_info in parsed["categories"].items():
        score = build_category_score(
            cat_name,
            cat_info["severity"],
            cat_info["severity_value"],
            threshold_map,
        )
        categories.append(score)
        if score.flagged:
            any_flagged = True
    return ModerationResult(
        text=text,
        categories=categories,
        highest_severity=parsed["highest_severity"],
        overall_flagged=any_flagged,
        blocklist_matches=parsed.get("blocklist_matches", []),
        raw_response=raw_response,
    )
