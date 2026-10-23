from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionSubmission:
    audio_url: Optional[str] = None
    audio_path: Optional[str] = None
    language_code: Optional[str] = None
    speaker_labels: bool = False
    speakers_expected: Optional[int] = None
    word_timestamps: bool = False
    punctuate: bool = True
    format_text: bool = True

    def to_assemblyai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "speaker_labels": self.speaker_labels,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
        }
        if self.audio_url:
            payload["audio_url"] = self.audio_url
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.speakers_expected is not None:
            payload["speakers_expected"] = self.speakers_expected
        if self.word_timestamps:
            payload["word_boost"] = []
        return payload


@dataclass
class TranscriptStatus:
    id: str
    status: str
    text: str = ""
    confidence: Optional[float] = None
    error: Optional[str] = None
    utterances: List[Dict[str, Any]] = field(default_factory=list)
    words: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_assemblyai(cls, data: Dict[str, Any]) -> "TranscriptStatus":
        return cls(
            id=data.get("id", ""),
            status=data.get("status", ""),
            text=data.get("text") or "",
            confidence=data.get("confidence"),
            error=data.get("error"),
            utterances=data.get("utterances") or [],
            words=data.get("words") or [],
        )


@dataclass
class TranscriptSegment:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None

    @classmethod
    def from_word(cls, word: Dict[str, Any]) -> "TranscriptSegment":
        return cls(
            text=word.get("text") or word.get("word") or "",
            start_ms=word.get("start"),
            end_ms=word.get("end"),
            speaker=word.get("speaker"),
            confidence=word.get("confidence"),
        )

    @classmethod
    def from_utterance(cls, utt: Dict[str, Any]) -> "TranscriptSegment":
        return cls(
            text=utt.get("text") or "",
            start_ms=utt.get("start"),
            end_ms=utt.get("end"),
            speaker=utt.get("speaker"),
            confidence=utt.get("confidence"),
        )


def normalize_segments(transcript: TranscriptStatus, granularity: str = "segment") -> List[TranscriptSegment]:
    if granularity == "word":
        return [TranscriptSegment.from_word(item) for item in transcript.words]
    if transcript.utterances:
        return [TranscriptSegment.from_utterance(item) for item in transcript.utterances]
    if transcript.words:
        return [TranscriptSegment.from_word(item) for item in transcript.words]
    if transcript.text:
        return [TranscriptSegment(text=transcript.text)]
    return []
