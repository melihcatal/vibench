from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


def _coerce_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _coerce_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _coerce_bool(value: Any) -> bool | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y", "on"}:
            return True
        if lowered in {"false", "0", "no", "n", "off"}:
            return False
    return bool(value)


def _coerce_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text != "" else None


def _coerce_mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    return dict(value)


@dataclass(frozen=True)
class TranscriptionRequest:
    audio_file_path: str
    model: str = "gpt-4o-transcribe"
    language: str | None = None
    prompt: str | None = None
    temperature: float | None = None
    timestamp_granularities: tuple[str, ...] = field(default_factory=tuple)
    extra_fields: dict[str, Any] = field(default_factory=dict)

    def to_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {"model": self.model, "audio_file_path": self.audio_file_path}
        if self.language is not None:
            kwargs["language"] = self.language
        if self.prompt is not None:
            kwargs["prompt"] = self.prompt
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        if self.timestamp_granularities:
            kwargs["timestamp_granularities"] = list(self.timestamp_granularities)
        kwargs.update(self.extra_fields)
        return kwargs


@dataclass(frozen=True)
class TranscriptSegment:
    start: float | None = None
    end: float | None = None
    text: str = ""
    speaker: str | None = None
    words: list[dict[str, Any]] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranscriptSegment":
        payload = dict(data)
        return cls(
            start=_coerce_float(payload.pop("start", None)),
            end=_coerce_float(payload.pop("end", None)),
            text=_coerce_str(payload.pop("text", None)) or _coerce_str(payload.pop("transcript", None)) or "",
            speaker=_coerce_str(payload.pop("speaker", None)),
            words=[dict(item) for item in payload.pop("words", []) or []],
            extra=payload,
        )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"text": self.text}
        if self.start is not None:
            data["start"] = self.start
        if self.end is not None:
            data["end"] = self.end
        if self.speaker is not None:
            data["speaker"] = self.speaker
        if self.words:
            data["words"] = [dict(word) for word in self.words]
        data.update(self.extra)
        return data


@dataclass(frozen=True)
class TranscriptWord:
    start: float | None = None
    end: float | None = None
    word: str = ""
    speaker: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranscriptWord":
        payload = dict(data)
        return cls(
            start=_coerce_float(payload.pop("start", None)),
            end=_coerce_float(payload.pop("end", None)),
            word=_coerce_str(payload.pop("word", None)) or _coerce_str(payload.pop("text", None)) or "",
            speaker=_coerce_str(payload.pop("speaker", None)),
            extra=payload,
        )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"word": self.word}
        if self.start is not None:
            data["start"] = self.start
        if self.end is not None:
            data["end"] = self.end
        if self.speaker is not None:
            data["speaker"] = self.speaker
        data.update(self.extra)
        return data


@dataclass(frozen=True)
class TranscriptionResponse:
    status: str | None = None
    text: str = ""
    model: str | None = None
    language: str | None = None
    duration: float | None = None
    segments: tuple[TranscriptSegment, ...] = field(default_factory=tuple)
    words: tuple[TranscriptWord, ...] = field(default_factory=tuple)
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TranscriptionResponse":
        payload = _coerce_mapping(data)
        segments = tuple(TranscriptSegment.from_dict(item) for item in payload.get("segments", []) or [])
        words = tuple(TranscriptWord.from_dict(item) for item in payload.get("words", []) or [])
        return cls(
            status=_coerce_str(payload.get("status")),
            text=_coerce_str(payload.get("text")) or _coerce_str(payload.get("transcript")) or "",
            model=_coerce_str(payload.get("model")),
            language=_coerce_str(payload.get("language")),
            duration=_coerce_float(payload.get("duration")),
            segments=segments,
            words=words,
            raw=payload,
        )

    def to_dict(self) -> dict[str, Any]:
        data = dict(self.raw)
        data["text"] = self.text
        if self.status is not None:
            data["status"] = self.status
        if self.model is not None:
            data["model"] = self.model
        if self.language is not None:
            data["language"] = self.language
        if self.duration is not None:
            data["duration"] = self.duration
        if self.segments:
            data["segments"] = [segment.to_dict() for segment in self.segments]
        if self.words:
            data["words"] = [word.to_dict() for word in self.words]
        return data


def normalize_transcription_result(result: Any) -> TranscriptionResponse:
    if isinstance(result, TranscriptionResponse):
        return result
    if hasattr(result, "model_dump"):
        return TranscriptionResponse.from_dict(result.model_dump())
    if hasattr(result, "model_dump_json"):
        import json

        return TranscriptionResponse.from_dict(json.loads(result.model_dump_json()))
    if isinstance(result, Mapping):
        return TranscriptionResponse.from_dict(result)
    raise TypeError(f"Unsupported transcription result type: {type(result)!r}")


def normalize_segments(result: Any) -> list[dict[str, Any]]:
    normalized = normalize_transcription_result(result)
    return [segment.to_dict() for segment in normalized.segments]


def normalize_words(result: Any) -> list[dict[str, Any]]:
    normalized = normalize_transcription_result(result)
    return [word.to_dict() for word in normalized.words]


def normalize_transcript_text(result: Any) -> str:
    return normalize_transcription_result(result).text
