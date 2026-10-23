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
    timestamps: bool = False
    webhook_url: Optional[str] = None

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "speaker_labels": self.speaker_labels,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
            "word_boost": [],
        }
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.timestamps:
            payload["disfluencies"] = False
        if self.webhook_url:
            payload["webhook_url"] = self.webhook_url
        return payload


@dataclass
class TranscriptSegment:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptionJob:
    transcript_id: str
    status: str
    text: str = ""
    language_code: Optional[str] = None
    audio_url: Optional[str] = None
    confidence: Optional[float] = None
    utterances: List[TranscriptSegment] = field(default_factory=list)
    words: List[TranscriptSegment] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_utterance(item: Dict[str, Any]) -> TranscriptSegment:
    return TranscriptSegment(
        text=item.get("text", ""),
        start_ms=item.get("start"),
        end_ms=item.get("end"),
        speaker=item.get("speaker"),
        confidence=item.get("confidence"),
        metadata={
            "words": item.get("words", []),
        },
    )


def normalize_word(item: Dict[str, Any]) -> TranscriptSegment:
    return TranscriptSegment(
        text=item.get("text", ""),
        start_ms=item.get("start"),
        end_ms=item.get("end"),
        confidence=item.get("confidence"),
        metadata={
            "speaker": item.get("speaker"),
        },
    )


def normalize_transcription(payload: Dict[str, Any]) -> TranscriptionJob:
    utterances = [normalize_utterance(item) for item in payload.get("utterances", [])]
    words = [normalize_word(item) for item in payload.get("words", [])]
    return TranscriptionJob(
        transcript_id=payload.get("id", ""),
        status=payload.get("status", "queued"),
        text=payload.get("text", "") or "",
        language_code=payload.get("language_code"),
        audio_url=payload.get("audio_url"),
        confidence=payload.get("confidence"),
        utterances=utterances,
        words=words,
        raw=payload,
    )
