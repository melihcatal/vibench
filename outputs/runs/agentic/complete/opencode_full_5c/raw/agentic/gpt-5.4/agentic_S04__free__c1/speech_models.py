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
    speaker_count: Optional[int] = None
    webhook_url: Optional[str] = None
    boost_phrases: List[str] = field(default_factory=list)

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
            "speaker_labels": self.speaker_labels,
        }
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.speaker_count is not None:
            payload["speakers_expected"] = self.speaker_count
        if self.webhook_url:
            payload["webhook_url"] = self.webhook_url
        if self.boost_phrases:
            payload["word_boost"] = self.boost_phrases
        return payload


@dataclass
class TranscriptSegment:
    start_ms: int
    end_ms: int
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class WordTimestamp:
    text: str
    start_ms: int
    end_ms: int
    confidence: Optional[float] = None
    speaker: Optional[str] = None


@dataclass
class BatchTranscriptionResult:
    transcript_id: str
    status: str
    text: str
    language_code: Optional[str] = None
    audio_duration: Optional[float] = None
    confidence: Optional[float] = None
    segments: List[TranscriptSegment] = field(default_factory=list)
    words: List[WordTimestamp] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_utterances(
    raw_utterances: Optional[List[Dict[str, Any]]],
) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    for utterance in raw_utterances or []:
        segments.append(
            TranscriptSegment(
                start_ms=int(utterance.get("start", 0)),
                end_ms=int(utterance.get("end", 0)),
                text=utterance.get("text", ""),
                speaker=str(utterance.get("speaker"))
                if utterance.get("speaker") is not None
                else None,
                confidence=utterance.get("confidence"),
            )
        )
    return segments


def normalize_words(raw_words: Optional[List[Dict[str, Any]]]) -> List[WordTimestamp]:
    words: List[WordTimestamp] = []
    for word in raw_words or []:
        words.append(
            WordTimestamp(
                text=word.get("text", ""),
                start_ms=int(word.get("start", 0)),
                end_ms=int(word.get("end", 0)),
                confidence=word.get("confidence"),
                speaker=str(word.get("speaker"))
                if word.get("speaker") is not None
                else None,
            )
        )
    return words


def normalize_transcription_result(payload: Dict[str, Any]) -> BatchTranscriptionResult:
    return BatchTranscriptionResult(
        transcript_id=payload.get("id", ""),
        status=payload.get("status", "queued"),
        text=payload.get("text", ""),
        language_code=payload.get("language_code"),
        audio_duration=payload.get("audio_duration"),
        confidence=payload.get("confidence"),
        segments=normalize_utterances(payload.get("utterances")),
        words=normalize_words(payload.get("words")),
        raw=payload,
    )
