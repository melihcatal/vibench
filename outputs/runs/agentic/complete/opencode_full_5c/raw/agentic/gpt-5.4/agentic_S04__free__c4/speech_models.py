from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TranscriptionJobRequest:
    audio_url: str
    language_code: str = "en_us"
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True

    def to_assemblyai_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "audio_url": self.audio_url,
            "language_code": self.language_code,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
        }
        if self.speaker_labels:
            payload["speaker_labels"] = True
        return payload


@dataclass(slots=True)
class TranscriptSegment:
    start_ms: int
    end_ms: int
    text: str
    speaker: str | None = None
    confidence: float | None = None
    words: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class TranscriptResult:
    transcript_id: str
    status: str
    text: str = ""
    segments: list[TranscriptSegment] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


def _normalize_word(word: dict[str, Any]) -> dict[str, Any]:
    return {
        "text": word.get("text", ""),
        "start_ms": word.get("start", 0),
        "end_ms": word.get("end", 0),
        "confidence": word.get("confidence"),
        "speaker": word.get("speaker"),
    }


def normalize_utterances(payload: dict[str, Any]) -> list[TranscriptSegment]:
    utterances = payload.get("utterances") or []
    segments: list[TranscriptSegment] = []
    for utterance in utterances:
        segments.append(
            TranscriptSegment(
                start_ms=utterance.get("start", 0),
                end_ms=utterance.get("end", 0),
                text=utterance.get("text", "").strip(),
                speaker=utterance.get("speaker"),
                confidence=utterance.get("confidence"),
                words=[_normalize_word(word) for word in utterance.get("words", [])],
            )
        )
    return segments


def normalize_words(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [_normalize_word(word) for word in payload.get("words") or []]


def normalize_transcript_result(payload: dict[str, Any]) -> TranscriptResult:
    segments = normalize_utterances(payload)
    if not segments and payload.get("words"):
        segments = [
            TranscriptSegment(
                start_ms=payload["words"][0].get("start", 0),
                end_ms=payload["words"][-1].get("end", 0),
                text=payload.get("text", "").strip(),
                words=normalize_words(payload),
            )
        ]
    return TranscriptResult(
        transcript_id=payload.get("id", ""),
        status=payload.get("status", "queued"),
        text=payload.get("text", ""),
        segments=segments,
        raw=payload,
    )
