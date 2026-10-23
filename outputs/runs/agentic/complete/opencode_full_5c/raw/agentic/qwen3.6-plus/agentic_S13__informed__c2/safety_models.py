from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CategoryScore:
    category: str
    score: float
    severity: str = ""


@dataclass
class SafetyResponse:
    text: str
    is_safe: bool
    category_scores: list[CategoryScore] = field(default_factory=list)
    flagged_categories: list[str] = field(default_factory=list)
    raw_response: Optional[dict] = None


@dataclass
class BatchModerationRequest:
    texts: list[str]


@dataclass
class BatchModerationResponse:
    results: list[SafetyResponse] = field(default_factory=list)

    @property
    def total_messages(self) -> int:
        return len(self.results)

    @property
    def flagged_count(self) -> int:
        return sum(1 for r in self.results if not r.is_safe)

    @property
    def safe_count(self) -> int:
        return sum(1 for r in self.results if r.is_safe)


@dataclass
class FlaggedSpan:
    start: int
    end: int
    category: str
    score: float
    original_text: str


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    flagged_spans: list[FlaggedSpan] = field(default_factory=list)
    is_safe: bool = True


@dataclass
class ThresholdConfig:
    hate_speech: float = 0.5
    self_harm: float = 0.5
    sexual: float = 0.5
    violence: float = 0.5
    default_threshold: float = 0.5

    def get_threshold(self, category: str) -> float:
        category_key = category.lower().replace(" ", "_").replace("-", "_")
        return getattr(self, category_key, self.default_threshold)


@dataclass
class ThresholdDecision:
    text: str
    allowed: bool
    reason: str
    scores: list[CategoryScore] = field(default_factory=list)
    thresholds_applied: dict[str, float] = field(default_factory=dict)


AZURE_CONTENT_SAFETY_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]

SEVERITY_MAP = {
    0: "Safe",
    2: "Low",
    4: "Medium",
    6: "High",
}


def normalize_azure_severity(severity_value: int) -> str:
    return SEVERITY_MAP.get(severity_value, "Unknown")


def normalize_azure_score(severity_value: int) -> float:
    return severity_value / 6.0


def build_azure_payload(text: str, categories: list[str] | None = None) -> dict:
    if categories is None:
        categories = AZURE_CONTENT_SAFETY_CATEGORIES
    return {
        "text": text,
        "categories": categories,
        "outputType": "FourSeverityLevels",
    }


def parse_azure_response(text: str, raw: dict) -> SafetyResponse:
    category_scores = []
    flagged_categories = []
    for cat_result in raw.get("categoriesAnalysis", []):
        cat_name = cat_result.get("category", "")
        severity = cat_result.get("severity", 0)
        score = normalize_azure_score(severity)
        severity_label = normalize_azure_severity(severity)
        category_scores.append(
            CategoryScore(
                category=cat_name,
                score=score,
                severity=severity_label,
            )
        )
        if severity >= 2:
            flagged_categories.append(cat_name)

    is_safe = len(flagged_categories) == 0
    return SafetyResponse(
        text=text,
        is_safe=is_safe,
        category_scores=category_scores,
        flagged_categories=flagged_categories,
        raw_response=raw,
    )
