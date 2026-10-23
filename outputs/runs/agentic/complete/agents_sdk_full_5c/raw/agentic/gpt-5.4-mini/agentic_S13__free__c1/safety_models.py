from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModerationRequest:
    text: str
    user_id: str | None = None

    def to_prompt(self) -> str:
        return json.dumps({"text": self.text, "user_id": self.user_id}, ensure_ascii=False)


@dataclass
class ModerationResult:
    allowed: bool
    categories: dict[str, Any] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    redactions: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ModerationBatchRequest:
    messages: list[str]

    def to_prompt(self) -> str:
        return json.dumps({"messages": self.messages}, ensure_ascii=False)


@dataclass
class ModerationBatchResult:
    decisions: list[dict[str, Any]]


@dataclass
class RedactionRequest:
    text: str

    def to_prompt(self) -> str:
        return json.dumps({"text": self.text}, ensure_ascii=False)


@dataclass
class RedactionResult:
    redacted_text: str
    spans: list[dict[str, Any]] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)


@dataclass
class ThresholdRequest:
    text: str
    thresholds: dict[str, float]

    def to_prompt(self) -> str:
        return json.dumps({"text": self.text, "thresholds": self.thresholds}, ensure_ascii=False)


@dataclass
class ThresholdResult:
    allowed: bool
    threshold_hits: list[dict[str, Any]] = field(default_factory=list)
    categories: dict[str, Any] = field(default_factory=dict)
    explanation: str = ""


@dataclass
class SummaryResult:
    summary: str


@dataclass
class TranslationResult:
    translated_text: str
    language: str


@dataclass
class EmbeddingResult:
    embedding: list[float]
    model: str


@dataclass
class AudioResult:
    audio_base64: str
    format: str = "mp3"


def _extract_text(payload: Any) -> str:
    if hasattr(payload, "output_text") and payload.output_text:
        return payload.output_text
    if hasattr(payload, "content") and payload.content:
        first = payload.content[0]
        return getattr(first, "text", str(first))
    if hasattr(payload, "choices") and payload.choices:
        choice = payload.choices[0]
        message = getattr(choice, "message", None)
        if message is not None:
            return getattr(message, "content", str(message))
    return str(payload)


def _loads(text: str) -> dict[str, Any]:
    return json.loads(text)


def normalize_moderation_response(payload: Any) -> ModerationResult:
    data = _loads(_extract_text(payload))
    return ModerationResult(**data)


def normalize_batch_response(payload: Any) -> ModerationBatchResult:
    data = _loads(_extract_text(payload))
    return ModerationBatchResult(decisions=data.get("decisions", data))


def normalize_redaction_response(payload: Any) -> RedactionResult:
    data = _loads(_extract_text(payload))
    return RedactionResult(**data)


def normalize_threshold_response(payload: Any) -> ThresholdResult:
    data = _loads(_extract_text(payload))
    return ThresholdResult(**data)
