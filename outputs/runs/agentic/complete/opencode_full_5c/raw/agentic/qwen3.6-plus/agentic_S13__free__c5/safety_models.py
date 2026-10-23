from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CategoryScore:
    category: str
    score: float
    flagged: bool


@dataclass
class ModerationResult:
    text: str
    flagged: bool
    categories: list[CategoryScore] = field(default_factory=list)
    highest_category: Optional[str] = None
    highest_score: float = 0.0
    raw_response: Optional[dict] = None


@dataclass
class BatchModerationResult:
    results: list[ModerationResult] = field(default_factory=list)

    @property
    def total_flagged(self) -> int:
        return sum(1 for r in self.results if r.flagged)

    @property
    def total_items(self) -> int:
        return len(self.results)


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    flagged_spans: list[dict] = field(default_factory=list)
    unsafe: bool = False


@dataclass
class ThresholdDecision:
    text: str
    allowed: bool
    exceeded_categories: list[str] = field(default_factory=list)
    scores: dict[str, float] = field(default_factory=dict)
    moderation_result: Optional[ModerationResult] = None


def normalize_category_scores(
    raw_categories: dict, raw_category_scores: dict
) -> list[CategoryScore]:
    scores = []
    for cat, flagged in raw_categories.items():
        score_value = raw_category_scores.get(cat, 0.0)
        scores.append(
            CategoryScore(
                category=cat,
                score=score_value,
                flagged=bool(flagged),
            )
        )
    return scores


def extract_highest(categories: list[CategoryScore]) -> tuple[Optional[str], float]:
    if not categories:
        return None, 0.0
    highest = max(categories, key=lambda c: c.score)
    return highest.category, highest.score


def parse_moderation_response(text: str, raw: dict) -> ModerationResult:
    result_obj = raw.get("results", [{}])[0]
    raw_categories = result_obj.get("categories", {})
    raw_scores = result_obj.get("category_scores", {})
    categories = normalize_category_scores(raw_categories, raw_scores)
    highest_cat, highest_score = extract_highest(categories)
    return ModerationResult(
        text=text,
        flagged=result_obj.get("flagged", False),
        categories=categories,
        highest_category=highest_cat,
        highest_score=highest_score,
        raw_response=raw,
    )


def parse_batch_moderation_response(
    texts: list[str], raw: dict
) -> BatchModerationResult:
    results = []
    raw_results = raw.get("results", [])
    for i, text in enumerate(texts):
        if i < len(raw_results):
            results.append(
                parse_moderation_response(text, {"results": [raw_results[i]]})
            )
        else:
            results.append(ModerationResult(text=text, flagged=False))
    return BatchModerationResult(results=results)
