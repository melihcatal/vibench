from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class CategoryScores:
    sexual: float = 0.0
    hate: float = 0.0
    harassment: float = 0.0
    self_harm: float = 0.0
    sexual_minors: float = 0.0
    hate_threatening: float = 0.0
    violence_graphic: float = 0.0
    self_harm_intent: float = 0.0
    self_harm_instructions: float = 0.0
    harassment_threatening: float = 0.0
    violence: float = 0.0

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_openai_response(cls, categories):
        mapping = {
            "sexual": "sexual",
            "hate": "hate",
            "harassment": "harassment",
            "self-harm": "self_harm",
            "sexual/minors": "sexual_minors",
            "hate/threatening": "hate_threatening",
            "violence/graphic": "violence_graphic",
            "self-harm/intent": "self_harm_intent",
            "self-harm/instructions": "self_harm_instructions",
            "harassment/threatening": "harassment_threatening",
            "violence": "violence",
        }
        kwargs = {}
        for api_key, attr_key in mapping.items():
            kwargs[attr_key] = float(categories.get(api_key, 0.0))
        return cls(**kwargs)


@dataclass
class CategoryFlags:
    sexual: bool = False
    hate: bool = False
    harassment: bool = False
    self_harm: bool = False
    sexual_minors: bool = False
    hate_threatening: bool = False
    violence_graphic: bool = False
    self_harm_intent: bool = False
    self_harm_instructions: bool = False
    harassment_threatening: bool = False
    violence: bool = False

    def to_dict(self):
        return asdict(self)

    def any_flagged(self):
        return any(asdict(self).values())

    def flagged_categories(self):
        return [k for k, v in asdict(self).items() if v]

    @classmethod
    def from_openai_response(cls, categories):
        mapping = {
            "sexual": "sexual",
            "hate": "hate",
            "harassment": "harassment",
            "self-harm": "self_harm",
            "sexual/minors": "sexual_minors",
            "hate/threatening": "hate_threatening",
            "violence/graphic": "violence_graphic",
            "self-harm/intent": "self_harm_intent",
            "self-harm/instructions": "self_harm_instructions",
            "harassment/threatening": "harassment_threatening",
            "violence": "violence",
        }
        kwargs = {}
        for api_key, attr_key in mapping.items():
            kwargs[attr_key] = bool(categories.get(api_key, False))
        return cls(**kwargs)


@dataclass
class ModerationResult:
    text: str
    flagged: bool
    categories: CategoryFlags
    category_scores: CategoryScores
    highest_score: float = 0.0
    highest_category: str = ""
    message_id: Optional[str] = None

    def to_dict(self):
        return {
            "text": self.text,
            "flagged": self.flagged,
            "categories": self.categories.to_dict(),
            "category_scores": self.category_scores.to_dict(),
            "highest_score": self.highest_score,
            "highest_category": self.highest_category,
            "message_id": self.message_id,
        }

    @classmethod
    def from_openai_response(cls, text, result, message_id=None):
        cats = CategoryFlags.from_openai_response(result.categories)
        scores = CategoryScores.from_openai_response(result.category_scores)
        score_dict = scores.to_dict()
        highest_cat = max(score_dict, key=score_dict.get) if score_dict else ""
        highest_val = score_dict.get(highest_cat, 0.0)
        return cls(
            text=text,
            flagged=result.flagged,
            categories=cats,
            category_scores=scores,
            highest_score=highest_val,
            highest_category=highest_cat,
            message_id=message_id,
        )


@dataclass
class ModerationRequest:
    text: str
    message_id: Optional[str] = None

    def to_dict(self):
        return {"text": self.text, "message_id": self.message_id}


@dataclass
class BatchModerationRequest:
    messages: list[ModerationRequest] = field(default_factory=list)

    def to_list(self):
        return [m.to_dict() for m in self.messages]

    @classmethod
    def from_texts(cls, texts, message_ids=None):
        if message_ids is None:
            message_ids = [None] * len(texts)
        messages = [
            ModerationRequest(text=t, message_id=mid)
            for t, mid in zip(texts, message_ids)
        ]
        return cls(messages=messages)


@dataclass
class ThresholdConfig:
    sexual: float = 0.5
    hate: float = 0.5
    harassment: float = 0.5
    self_harm: float = 0.5
    sexual_minors: float = 0.3
    hate_threatening: float = 0.3
    violence_graphic: float = 0.3
    self_harm_intent: float = 0.3
    self_harm_instructions: float = 0.3
    harassment_threatening: float = 0.3
    violence: float = 0.5

    def to_dict(self):
        return asdict(self)

    @classmethod
    def strict(cls):
        return cls(
            sexual=0.3,
            hate=0.3,
            harassment=0.3,
            self_harm=0.3,
            sexual_minors=0.1,
            hate_threatening=0.1,
            violence_graphic=0.1,
            self_harm_intent=0.1,
            self_harm_instructions=0.1,
            harassment_threatening=0.1,
            violence=0.3,
        )

    @classmethod
    def permissive(cls):
        return cls(
            sexual=0.8,
            hate=0.8,
            harassment=0.8,
            self_harm=0.8,
            sexual_minors=0.6,
            hate_threatening=0.6,
            violence_graphic=0.6,
            self_harm_intent=0.6,
            self_harm_instructions=0.6,
            harassment_threatening=0.6,
            violence=0.8,
        )


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    flagged_segments: list = field(default_factory=list)
    categories_triggered: list = field(default_factory=list)

    def to_dict(self):
        return {
            "original_text": self.original_text,
            "redacted_text": self.redacted_text,
            "flagged_segments": self.flagged_segments,
            "categories_triggered": self.categories_triggered,
        }


@dataclass
class ModerationSummary:
    total_messages: int = 0
    flagged_count: int = 0
    allowed_count: int = 0
    top_categories: dict = field(default_factory=dict)
    average_scores: dict = field(default_factory=dict)
    summary_text: str = ""

    def to_dict(self):
        return {
            "total_messages": self.total_messages,
            "flagged_count": self.flagged_count,
            "allowed_count": self.allowed_count,
            "top_categories": self.top_categories,
            "average_scores": self.average_scores,
            "summary_text": self.summary_text,
        }


@dataclass
class AppealTranslation:
    original_text: str
    target_language: str
    translated_text: str
    source_language_detected: str = ""

    def to_dict(self):
        return {
            "original_text": self.original_text,
            "target_language": self.target_language,
            "translated_text": self.translated_text,
            "source_language_detected": self.source_language_detected,
        }


@dataclass
class EmbeddingResult:
    text: str
    embedding: list[float] = field(default_factory=list)
    model: str = ""
    usage_tokens: int = 0

    def to_dict(self):
        return {
            "text": self.text,
            "embedding": self.embedding,
            "model": self.model,
            "usage_tokens": self.usage_tokens,
        }


@dataclass
class AudioBriefResult:
    text: str
    audio_bytes: bytes = b""
    voice: str = ""
    model: str = ""
    format: str = ""

    def to_dict(self):
        return {
            "text": self.text,
            "voice": self.voice,
            "model": self.model,
            "format": self.format,
            "audio_size_bytes": len(self.audio_bytes),
        }
