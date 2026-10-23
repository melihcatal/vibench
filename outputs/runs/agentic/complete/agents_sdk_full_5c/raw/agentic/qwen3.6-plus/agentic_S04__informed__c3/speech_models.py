"""
Local request, response, and normalization helpers for AssemblyAI Batch Speech-to-Text.

Defines dataclasses and helper functions for standardizing
AssemblyAI Transcripts API payloads and responses.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from enum import Enum


class TranscriptionStatus(str, Enum):
    """AssemblyAI transcription job statuses."""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class TranscriptionRequest:
    """
    Request model for submitting audio to AssemblyAI.

    Maps to AssemblyAI's Transcriber configuration schema.
    """
    audio_url: str
    language_code: str = "en"
    punctuate: bool = True
    format_text: bool = True
    speaker_labels: bool = False
    word_timestamps: bool = False
    speakers_expected: Optional[int] = None
    auto_chapters: bool = False
    entity_detection: bool = False
    custom_spelling: Optional[List[Dict[str, List[str]]]] = None

    def to_assemblyai_config(self) -> Dict[str, Any]:
        """Convert to AssemblyAI Transcriber config dict."""
        config: Dict[str, Any] = {
            "audio_url": self.audio_url,
            "language_code": self.language_code,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
        }
        if self.speaker_labels:
            config["speaker_labels"] = True
        if self.word_timestamps:
            config["word_timestamps"] = True
        if self.speakers_expected is not None:
            config["speakers_expected"] = self.speakers_expected
        if self.auto_chapters:
            config["auto_chapters"] = True
        if self.entity_detection:
            config["entity_detection"] = True
        if self.custom_spelling:
            config["custom_spelling"] = self.custom_spelling
        return config


@dataclass
class WordTimestamp:
    """Word-level timestamp from AssemblyAI."""
    text: str
    start: int  # milliseconds
    end: int
    confidence: float
    speaker: Optional[str] = None

    @classmethod
    def from_assemblyai_word(cls, word: Dict[str, Any]) -> "WordTimestamp":
        return cls(
            text=word.get("text", ""),
            start=word.get("start", 0),
            end=word.get("end", 0),
            confidence=word.get("confidence", 0.0),
            speaker=word.get("speaker"),
        )


@dataclass
class Utterance:
    """Speaker utterance from AssemblyAI diarization."""
    speaker: str
    text: str
    start: int
    end: int
    confidence: float
    words: List[WordTimestamp] = field(default_factory=list)

    @classmethod
    def from_assemblyai_utterance(cls, utt: Dict[str, Any]) -> "Utterance":
        words = [
            WordTimestamp.from_assemblyai_word(w)
            for w in utt.get("words", [])
        ]
        return cls(
            speaker=utt.get("speaker", "unknown"),
            text=utt.get("text", ""),
            start=utt.get("start", 0),
            end=utt.get("end", 0),
            confidence=utt.get("confidence", 0.0),
            words=words,
        )


@dataclass
class TranscriptionResult:
    """
    Normalized transcription result from AssemblyAI.

    Standardizes the AssemblyAI response into a consistent local format.
    """
    transcript_id: str
    status: TranscriptionStatus
    text: str
    words: List[WordTimestamp] = field(default_factory=list)
    utterances: List[Utterance] = field(default_factory=list)
    language: str = ""
    audio_duration: Optional[float] = None
    confidence: Optional[float] = None
    error: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

    @classmethod
    def from_assemblyai_response(cls, response: Dict[str, Any]) -> "TranscriptionResult":
        """Parse raw AssemblyAI API response into TranscriptionResult."""
        status_str = response.get("status", "unknown")
        try:
            status = TranscriptionStatus(status_str)
        except ValueError:
            status = TranscriptionStatus(status_str)

        words = [
            WordTimestamp.from_assemblyai_word(w)
            for w in response.get("words", [])
        ]
        utterances = [
            Utterance.from_assemblyai_utterance(u)
            for u in response.get("utterances", [])
        ]

        return cls(
            transcript_id=response.get("id", ""),
            status=status,
            text=response.get("text", ""),
            words=words,
            utterances=utterances,
            language=response.get("language_code", ""),
            audio_duration=response.get("audio_duration"),
            confidence=response.get("confidence"),
            error=response.get("error"),
            raw_response=response,
        )

    @property
    def is_completed(self) -> bool:
        return self.status == TranscriptionStatus.COMPLETED

    @property
    def is_error(self) -> bool:
        return self.status == TranscriptionStatus.ERROR

    @property
    def is_processing(self) -> bool:
        return self.status in (TranscriptionStatus.QUEUED, TranscriptionStatus.PROCESSING)


@dataclass
class DiarizedTranscript:
    """Speaker-diarized transcript output."""
    transcript_id: str
    speakers: List[str]
    utterances: List[Utterance]
    full_text: str

    @classmethod
    def from_transcription_result(cls, result: TranscriptionResult) -> "DiarizedTranscript":
        speakers = list(set(u.speaker for u in result.utterances if u.speaker))
        return cls(
            transcript_id=result.transcript_id,
            speakers=sorted(speakers),
            utterances=result.utterances,
            full_text=result.text,
        )


@dataclass
class TimestampedSegment:
    """Segment with word-level timestamps."""
    text: str
    start_ms: int
    end_ms: int
    words: List[WordTimestamp]

    @classmethod
    def from_utterance(cls, utterance: Utterance) -> "TimestampedSegment":
        return cls(
            text=utterance.text,
            start_ms=utterance.start,
            end_ms=utterance.end,
            words=utterance.words,
        )
