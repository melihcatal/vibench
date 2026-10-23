from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BatchTranscriptionRequest:
    audio_url: str
    language_code: str = "en_us"
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True
    disfluencies: bool = False
    custom_spelling: Optional[List[Dict[str, str]]] = None
    webhook_url: Optional[str] = None

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "language_code": self.language_code,
            "speaker_labels": self.speaker_labels,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
            "disfluencies": self.disfluencies,
        }
        if self.custom_spelling:
            payload["custom_spelling"] = self.custom_spelling
        if self.webhook_url:
            payload["webhook_url"] = self.webhook_url
        return payload


@dataclass
class TranscriptSegment:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptResult:
    transcript_id: str
    status: str
    text: str = ""
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    segments: List[TranscriptSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_utterances(raw: Dict[str, Any]) -> List[TranscriptSegment]:
    utterances = raw.get("utterances") or []
    normalized: List[TranscriptSegment] = []
    for item in utterances:
        normalized.append(
            TranscriptSegment(
                text=item.get("text", ""),
                start=item.get("start"),
                end=item.get("end"),
                speaker=str(item.get("speaker")) if item.get("speaker") is not None else None,
                confidence=item.get("confidence"),
                metadata={
                    "words": item.get("words", []),
                },
            )
        )
    return normalized


def normalize_words(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    words = raw.get("words") or []
    normalized: List[Dict[str, Any]] = []
    for word in words:
        normalized.append(
            {
                "text": word.get("text") or word.get("word") or "",
                "start": word.get("start"),
                "end": word.get("end"),
                "confidence": word.get("confidence"),
                "speaker": word.get("speaker"),
            }
        )
    return normalized


def normalize_transcript(raw: Dict[str, Any]) -> TranscriptResult:
    return TranscriptResult(
        transcript_id=raw.get("id", ""),
        status=raw.get("status", "queued"),
        text=raw.get("text") or "",
        confidence=raw.get("confidence"),
        language_code=raw.get("language_code"),
        segments=normalize_utterances(raw),
        raw=raw,
    )
