from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class SafetyCategory(str, enum.Enum):
    HATE = "hate"
    HATE_THREATENING = "hate/threatening"
    SELF_HARM = "self-harm"
    SELF_HARM_INTENT = "self-harm/intent"
    SELF_HARM_INSTRUCTIONS = "self-harm/instructions"
    SEXUAL = "sexual"
    SEXUAL_MINORS = "sexual/minors"
    VIOLENCE = "violence"
    VIOLENCE_GRAPHIC = "violence/graphic"
    HARASSMENT = "harassment"
    HARASSMENT_THREATENING = "harassment/threatening"
    ILLEGAL = "illegal"
    ILLEGAL_DRUGS = "illegal/drugs"
    PROFANITY = "profanity"


class ModerationAction(str, enum.Enum):
    ALLOW = "allow"
    FLAG = "flag"
    REDACT = "redact"
    BLOCK = "block"


@dataclass
class CategoryScore:
    category: str
    score: float
    flagged: bool
    severity: str = "unknown"

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "score": self.score,
            "flagged": self.flagged,
            "severity": self.severity,
        }


@dataclass
class ModerationResult:
    text: str
    flagged: bool
    action: ModerationAction
    categories: list[CategoryScore]
    highest_score: float = 0.0
    rationale: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "flagged": self.flagged,
            "action": self.action.value,
            "categories": [c.to_dict() for c in self.categories],
            "highest_score": self.highest_score,
            "rationale": self.rationale,
            "metadata": self.metadata,
        }


@dataclass
class BatchModerationResult:
    results: list[ModerationResult]
    total_flagged: int = 0
    total_processed: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "results": [r.to_dict() for r in self.results],
            "total_flagged": self.total_flagged,
            "total_processed": self.total_processed,
        }


@dataclass
class RedactionSpan:
    start: int
    end: int
    category: str
    original_text: str
    replacement: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "start": self.start,
            "end": self.end,
            "category": self.category,
            "original_text": self.original_text,
            "replacement": self.replacement,
        }


@dataclass
class RedactedText:
    original: str
    redacted: str
    spans: list[RedactionSpan]
    was_modified: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "original": self.original,
            "redacted": self.redacted,
            "spans": [s.to_dict() for s in self.spans],
            "was_modified": self.was_modified,
        }


@dataclass
class ThresholdDecision:
    text: str
    allowed: bool
    category_scores: list[CategoryScore]
    threshold_applied: dict[str, float]
    exceeded_categories: list[str]
    rationale: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "allowed": self.allowed,
            "category_scores": [c.to_dict() for c in self.category_scores],
            "threshold_applied": self.threshold_applied,
            "exceeded_categories": self.exceeded_categories,
            "rationale": self.rationale,
        }


@dataclass
class ModerationSummary:
    total_items: int
    flagged_count: int
    allowed_count: int
    blocked_count: int
    category_breakdown: dict[str, int]
    severity_distribution: dict[str, int]
    top_violations: list[dict[str, Any]]
    summary_text: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_items": self.total_items,
            "flagged_count": self.flagged_count,
            "allowed_count": self.allowed_count,
            "blocked_count": self.blocked_count,
            "category_breakdown": self.category_breakdown,
            "severity_distribution": self.severity_distribution,
            "top_violations": self.top_violations,
            "summary_text": self.summary_text,
        }


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "provider": self.provider,
        }


@dataclass
class EmbeddingResult:
    text: str
    embedding: list[float]
    model: str
    dimensions: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "embedding": self.embedding,
            "model": self.model,
            "dimensions": self.dimensions,
        }


@dataclass
class AudioResult:
    text: str
    audio_url: str
    audio_format: str
    duration_seconds: float
    model: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "audio_url": self.audio_url,
            "audio_format": self.audio_format,
            "duration_seconds": self.duration_seconds,
            "model": self.model,
        }


def normalize_openai_categories(raw: dict[str, Any]) -> list[CategoryScore]:
    category_map = {
        "hate": SafetyCategory.HATE,
        "hate/threatening": SafetyCategory.HATE_THREATENING,
        "self-harm": SafetyCategory.SELF_HARM,
        "self-harm/intent": SafetyCategory.SELF_HARM_INTENT,
        "self-harm/instructions": SafetyCategory.SELF_HARM_INSTRUCTIONS,
        "sexual": SafetyCategory.SEXUAL,
        "sexual/minors": SafetyCategory.SEXUAL_MINORS,
        "violence": SafetyCategory.VIOLENCE,
        "violence/graphic": SafetyCategory.VIOLENCE_GRAPHIC,
        "harassment": SafetyCategory.HARASSMENT,
        "harassment/threatening": SafetyCategory.HARASSMENT_THREATENING,
    }
    scores: list[CategoryScore] = []
    for cat_key, score_val in raw.items():
        if cat_key not in category_map:
            continue
        enum_cat = category_map[cat_key]
        flagged = score_val > 0.5
        if score_val >= 0.8:
            severity = "high"
        elif score_val >= 0.5:
            severity = "medium"
        elif score_val >= 0.2:
            severity = "low"
        else:
            severity = "negligible"
        scores.append(
            CategoryScore(
                category=enum_cat.value,
                score=round(score_val, 4),
                flagged=flagged,
                severity=severity,
            )
        )
    return scores


def normalize_perspective_categories(raw: dict[str, float]) -> list[CategoryScore]:
    scores: list[CategoryScore] = []
    for cat_key, score_val in raw.items():
        flagged = score_val > 0.5
        if score_val >= 0.8:
            severity = "high"
        elif score_val >= 0.5:
            severity = "medium"
        elif score_val >= 0.2:
            severity = "low"
        else:
            severity = "negligible"
        scores.append(
            CategoryScore(
                category=cat_key,
                score=round(score_val, 4),
                flagged=flagged,
                severity=severity,
            )
        )
    return scores


def normalize_azure_categories(raw: dict[str, float]) -> list[CategoryScore]:
    azure_map = {
        "Hate": SafetyCategory.HATE,
        "SelfHarm": SafetyCategory.SELF_HARM,
        "Sexual": SafetyCategory.SEXUAL,
        "Violence": SafetyCategory.VIOLENCE,
    }
    scores: list[CategoryScore] = []
    for cat_key, score_val in raw.items():
        enum_cat = azure_map.get(cat_key)
        if enum_cat is None:
            enum_cat_name = cat_key.lower().replace("_", "/")
        else:
            enum_cat_name = enum_cat.value
        flagged = score_val > 0.5
        if score_val >= 0.8:
            severity = "high"
        elif score_val >= 0.5:
            severity = "medium"
        elif score_val >= 0.2:
            severity = "low"
        else:
            severity = "negligible"
        scores.append(
            CategoryScore(
                category=enum_cat_name,
                score=round(score_val, 4),
                flagged=flagged,
                severity=severity,
            )
        )
    return scores


def determine_action(flagged: bool, highest_score: float) -> ModerationAction:
    if not flagged:
        return ModerationAction.ALLOW
    if highest_score >= 0.85:
        return ModerationAction.BLOCK
    if highest_score >= 0.6:
        return ModerationAction.REDACT
    return ModerationAction.FLAG
