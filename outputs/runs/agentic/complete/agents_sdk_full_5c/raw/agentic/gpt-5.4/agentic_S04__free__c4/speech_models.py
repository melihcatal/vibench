from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BatchTranscriptionRequest:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "speaker_labels": self.speaker_labels,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
        }
        if self.language_code:
            payload["language_code"] = self.language_code
        return payload


@dataclass
class TranscriptJob:
    transcript_id: str
    status: str
    text: str = ""
    utterances: List[Dict[str, Any]] = field(default_factory=list)
    words: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class TranscriptSegment:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[str] = None


@dataclass
class TranslationSegment:
    source_text: str
    translated_text: str
    target_language: str


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]


@dataclass
class SummaryResult:
    summary: str
    model: str


@dataclass
class EmbeddingVector:
    text: str
    vector: List[float]
    model: str


def normalize_assemblyai_transcript(payload: Dict[str, Any]) -> TranscriptJob:
    return TranscriptJob(
        transcript_id=str(payload.get("id", "")),
        status=str(payload.get("status", "")),
        text=payload.get("text") or "",
        utterances=payload.get("utterances") or [],
        words=payload.get("words") or [],
        error=payload.get("error"),
    )


def transcript_segments_from_utterances(utterances: List[Dict[str, Any]]) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    for item in utterances:
        segments.append(
            TranscriptSegment(
                text=item.get("text", ""),
                start_ms=item.get("start"),
                end_ms=item.get("end"),
                speaker=item.get("speaker"),
            )
        )
    return segments


def transcript_segments_from_words(words: List[Dict[str, Any]]) -> List[TranscriptSegment]:
    return [
        TranscriptSegment(
            text=item.get("text", ""),
            start_ms=item.get("start"),
            end_ms=item.get("end"),
            speaker=item.get("speaker"),
        )
        for item in words
    ]
