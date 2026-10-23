from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class TranscriptionStatus(Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class TranscriptionRequest:
    audio_url: str
    language_code: str = "en"
    speaker_labels: bool = True
    punctuate: bool = True
    format_text: bool = True
    speakers_expected: Optional[int] = None
    custom_vocabulary: Optional[List[str]] = None


@dataclass
class WordTimestamp:
    text: str
    start: int  # milliseconds
    end: int  # milliseconds
    confidence: float


@dataclass
class SegmentTimestamp:
    text: str
    start: int  # milliseconds
    end: int  # milliseconds
    speaker: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class TranscriptionResult:
    job_id: str
    status: TranscriptionStatus
    text: Optional[str] = None
    words: List[WordTimestamp] = None
    utterances: List[SegmentTimestamp] = None
    confidence: Optional[float] = None
    audio_duration: Optional[int] = None
    error: Optional[str] = None
    provider: str = "AssemblyAI"

    def __post_init__(self):
        if self.words is None:
            self.words = []
        if self.utterances is None:
            self.utterances = []


@dataclass
class DiarizationResult:
    job_id: str
    status: TranscriptionStatus
    diarized_segments: List[SegmentTimestamp]
    speaker_count: int
    error: Optional[str] = None
    provider: str = "AssemblyAI"


def normalize_assemblyai_transcript(transcript) -> TranscriptionResult:
    """Convert AssemblyAI transcript to standardized format."""
    if not transcript:
        return None

    status_map = {
        "queued": TranscriptionStatus.QUEUED,
        "processing": TranscriptionStatus.PROCESSING,
        "completed": TranscriptionStatus.COMPLETED,
        "error": TranscriptionStatus.ERROR,
    }

    status = status_map.get(transcript.status.value, TranscriptionStatus.ERROR)

    words = []
    if transcript.words:
        words = [
            WordTimestamp(
                text=word.text,
                start=int(word.start),
                end=int(word.end),
                confidence=word.confidence,
            )
            for word in transcript.words
        ]

    utterances = []
    if transcript.utterances:
        utterances = [
            SegmentTimestamp(
                text=utterance.text,
                start=int(utterance.start),
                end=int(utterance.end),
                speaker=utterance.speaker,
                confidence=utterance.confidence,
            )
            for utterance in transcript.utterances
        ]

    return TranscriptionResult(
        job_id=transcript.id,
        status=status,
        text=transcript.text,
        words=words,
        utterances=utterances,
        confidence=transcript.confidence,
        audio_duration=transcript.audio_duration,
        error=transcript.error if status == TranscriptionStatus.ERROR else None,
        provider="AssemblyAI",
    )
