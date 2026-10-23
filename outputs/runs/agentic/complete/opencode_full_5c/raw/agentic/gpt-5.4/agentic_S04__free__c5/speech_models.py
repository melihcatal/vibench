from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionSubmission:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    webhook_url: Optional[str] = None
    word_boost: List[str] = field(default_factory=list)

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "speaker_labels": self.speaker_labels,
        }
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.webhook_url:
            payload["webhook_url"] = self.webhook_url
        if self.word_boost:
            payload["word_boost"] = self.word_boost
        return payload


@dataclass
class TranscriptStatus:
    id: str
    status: str
    text: str = ""
    words: List[Dict[str, Any]] = field(default_factory=list)
    utterances: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class TranscriptSegment:
    start_ms: int
    end_ms: int
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class TranslationResult:
    translated_segments: List[Dict[str, Any]]
    provider: str
    target_language: str


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    provider: str


@dataclass
class SummaryResult:
    summary: str
    provider: str
    model: str


@dataclass
class EmbeddingResult:
    vectors: List[List[float]]
    provider: str
    model: str


def normalize_transcript_response(payload: Dict[str, Any]) -> TranscriptStatus:
    return TranscriptStatus(
        id=payload.get("id", ""),
        status=payload.get("status", "queued"),
        text=payload.get("text", "") or "",
        words=payload.get("words", []) or [],
        utterances=payload.get("utterances", []) or [],
        error=payload.get("error"),
    )


def transcript_segments_from_utterances(
    utterances: List[Dict[str, Any]],
) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    for item in utterances:
        segments.append(
            TranscriptSegment(
                start_ms=int(item.get("start", 0)),
                end_ms=int(item.get("end", 0)),
                text=item.get("text", "") or "",
                speaker=item.get("speaker"),
                confidence=item.get("confidence"),
            )
        )
    return segments


def transcript_segments_from_words(
    words: List[Dict[str, Any]],
) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    for item in words:
        segments.append(
            TranscriptSegment(
                start_ms=int(item.get("start", 0)),
                end_ms=int(item.get("end", 0)),
                text=item.get("text", "") or "",
                confidence=item.get("confidence"),
            )
        )
    return segments


def segment_dicts(segments: List[TranscriptSegment]) -> List[Dict[str, Any]]:
    return [
        {
            "start_ms": segment.start_ms,
            "end_ms": segment.end_ms,
            "text": segment.text,
            "speaker": segment.speaker,
            "confidence": segment.confidence,
        }
        for segment in segments
    ]
