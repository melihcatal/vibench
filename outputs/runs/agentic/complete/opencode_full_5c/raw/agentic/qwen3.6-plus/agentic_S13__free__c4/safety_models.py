from dataclasses import dataclass, field
from typing import Optional
import math


@dataclass
class ModerationRequest:
    text: str
    categories: Optional[list] = None


@dataclass
class CategoryScore:
    name: str
    score: float
    flagged: bool


@dataclass
class ModerationResult:
    flagged: bool
    categories: list
    category_scores: list
    raw_response: Optional[dict] = None


@dataclass
class BatchModerationRequest:
    texts: list


@dataclass
class BatchModerationResult:
    results: list
    total: int
    flagged_count: int


@dataclass
class RedactionResult:
    original: str
    redacted: str
    flagged_spans: list
    categories_found: list


@dataclass
class ThresholdConfig:
    hate: float = 0.5
    hate_threatening: float = 0.5
    self_harm: float = 0.5
    sexual: float = 0.5
    sexual_minors: float = 0.3
    violence: float = 0.5
    violence_graphic: float = 0.5
    harassment: float = 0.5
    harassment_threatening: float = 0.5
    illicit: float = 0.5
    illicit_violent: float = 0.5
    self_harm_intent: float = 0.5
    self_harm_instructions: float = 0.3
    sexualizing_minors: float = 0.3


@dataclass
class ThresholdDecision:
    allowed: bool
    exceeded_categories: list
    scores: dict


@dataclass
class ModerationSummary:
    total_analyzed: int
    total_flagged: int
    total_allowed: int
    category_breakdown: dict
    top_violations: list
    summary_text: str


@dataclass
class AppealTranslation:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class EmbeddingResult:
    text: str
    embedding: list
    model: str
    usage: dict


@dataclass
class AudioBrief:
    text: str
    audio_bytes: bytes
    format: str
    duration_estimate: float


DEFAULT_CATEGORIES = [
    "hate",
    "hate/threatening",
    "self-harm",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
    "harassment",
    "harassment/threatening",
    "illicit",
    "illicit/violent",
    "self-harm/intent",
    "self-harm/instructions",
    "sexualizing/minors",
]


def normalize_category_name(raw_name):
    return raw_name.replace("/", "_").replace("-", "_").lower()


def normalize_moderation_response(raw_response):
    result = (
        raw_response.results[0] if hasattr(raw_response, "results") else raw_response
    )
    flagged = result.flagged
    category_scores = []
    categories = []
    for cat_name, flagged_value in result.categories.items():
        norm_name = normalize_category_name(cat_name)
        if flagged_value:
            categories.append(norm_name)
    for cat_name, score_value in result.category_scores.items():
        norm_name = normalize_category_name(cat_name)
        category_scores.append(
            CategoryScore(
                name=norm_name,
                score=float(score_value),
                flagged=cat_name.replace("/", "_").replace("-", "_").lower()
                in categories,
            )
        )
    return ModerationResult(
        flagged=flagged,
        categories=categories,
        category_scores=category_scores,
        raw_response={
            "flagged": flagged,
            "categories": dict(result.categories),
            "category_scores": dict(result.category_scores),
        },
    )


def compute_risk_score(category_scores):
    if not category_scores:
        return 0.0
    max_score = max(cs.score for cs in category_scores)
    avg_score = sum(cs.score for cs in category_scores) / len(category_scores)
    flagged_count = sum(1 for cs in category_scores if cs.flagged)
    return round(min(1.0, (max_score * 0.5 + avg_score * 0.3 + flagged_count * 0.2)), 4)


def truncate_text(text, max_length=4000):
    if len(text) <= max_length:
        return text
    return text[: max_length - 100] + "\n... [truncated]"
