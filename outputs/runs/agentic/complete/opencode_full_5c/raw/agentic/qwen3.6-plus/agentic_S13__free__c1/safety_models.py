from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ModerationRequest:
    text: str
    request_id: Optional[str] = None


@dataclass
class CategoryScore:
    category: str
    score: float
    flagged: bool


@dataclass
class ModerationResult:
    text: str
    flagged: bool
    category_scores: list[CategoryScore]
    request_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "flagged": self.flagged,
            "category_scores": [asdict(cs) for cs in self.category_scores],
            "request_id": self.request_id,
        }


@dataclass
class BatchModerationRequest:
    texts: list[str]
    request_id: Optional[str] = None


@dataclass
class BatchModerationResult:
    results: list[ModerationResult]
    request_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "results": [r.to_dict() for r in self.results],
            "request_id": self.request_id,
        }


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    flagged_spans: list[dict]
    overall_flagged: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ThresholdDecision:
    text: str
    allowed: bool
    category_scores: list[CategoryScore]
    applied_thresholds: dict[str, float]
    request_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "allowed": self.allowed,
            "category_scores": [asdict(cs) for cs in self.category_scores],
            "applied_thresholds": self.applied_thresholds,
            "request_id": self.request_id,
        }


@dataclass
class ModerationSummary:
    total_texts: int
    flagged_count: int
    safe_count: int
    top_categories: list[dict]
    summary_text: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AppealTranslation:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReasonEmbedding:
    text: str
    embedding: list[float]
    model: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AudioBrief:
    text_content: str
    audio_bytes: bytes
    model: str
    voice: str

    def to_dict(self) -> dict:
        return {
            "text_content": self.text_content,
            "model": self.model,
            "voice": self.voice,
            "audio_size_bytes": len(self.audio_bytes),
        }


def normalize_category_scores(
    raw_categories: dict, raw_scores: dict
) -> list[CategoryScore]:
    return [
        CategoryScore(
            category=cat,
            score=raw_scores.get(cat, 0.0),
            flagged=raw_categories.get(cat, False),
        )
        for cat in sorted(raw_categories.keys())
    ]
