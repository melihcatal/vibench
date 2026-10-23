from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class TranscriptionStatus(Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TranscriptionRequest:
    audio_file_path: str
    language: Optional[str] = None
    model: str = "whisper-1"
    response_format: str = "json"
    temperature: float = 0.0
    prompt: Optional[str] = None


@dataclass
class TranscriptionJob:
    job_id: str
    status: TranscriptionStatus
    audio_url: Optional[str] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None


@dataclass
class WordSegment:
    word: str
    start: float
    end: float
    confidence: float = 1.0
    speaker: Optional[str] = None


@dataclass
class TranscriptSegment:
    text: str
    start: float
    end: float
    words: list[WordSegment] = field(default_factory=list)
    speaker: Optional[str] = None


@dataclass
class TranscriptionResult:
    job_id: str
    text: str
    segments: list[TranscriptSegment] = field(default_factory=list)
    language: Optional[str] = None
    duration: Optional[float] = None


@dataclass
class DiarizationResult:
    job_id: str
    text: str
    segments: list[TranscriptSegment] = field(default_factory=list)
    speakers: list[str] = field(default_factory=list)


@dataclass
class TimestampedResult:
    job_id: str
    text: str
    words: list[WordSegment] = field(default_factory=list)
    segments: list[TranscriptSegment] = field(default_factory=list)


@dataclass
class TranslationRequest:
    segments: list[TranscriptSegment]
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResult:
    segments: list[TranscriptSegment]
    target_language: str


@dataclass
class ModerationResult:
    flagged: bool
    categories: dict[str, bool] = field(default_factory=dict)
    category_scores: dict[str, float] = field(default_factory=dict)
    flagged_segments: list[int] = field(default_factory=list)


@dataclass
class ArchiveSummary:
    job_id: str
    total_segments: int
    total_words: int
    duration_seconds: float
    language: str
    summary_text: str
    key_topics: list[str] = field(default_factory=list)


@dataclass
class EmbeddingResult:
    segment_index: int
    text: str
    embedding: list[float]
    model: str


def normalize_transcription_response(raw: dict) -> TranscriptionResult:
    segments = []
    for seg in raw.get("segments", []):
        words = [
            WordSegment(
                word=w["word"],
                start=w["start"],
                end=w["end"],
                confidence=w.get("confidence", 1.0),
            )
            for w in seg.get("words", [])
        ]
        segments.append(
            TranscriptSegment(
                text=seg["text"],
                start=seg["start"],
                end=seg["end"],
                words=words,
            )
        )
    return TranscriptionResult(
        job_id=raw.get("id", raw.get("job_id", "")),
        text=raw.get("text", ""),
        segments=segments,
        language=raw.get("language"),
        duration=raw.get("duration"),
    )


def normalize_diarization_response(raw: dict) -> DiarizationResult:
    segments = []
    speakers = set()
    for seg in raw.get("utterances", raw.get("segments", [])):
        speaker = seg.get("speaker", seg.get("channel", "unknown"))
        speakers.add(speaker)
        segments.append(
            TranscriptSegment(
                text=seg["text"],
                start=seg.get("start", 0.0),
                end=seg.get("end", 0.0),
                speaker=speaker,
            )
        )
    return DiarizationResult(
        job_id=raw.get("id", raw.get("job_id", "")),
        text=raw.get("text", ""),
        segments=segments,
        speakers=sorted(speakers),
    )


def normalize_timestamp_response(raw: dict) -> TimestampedResult:
    words = []
    segments = []
    for seg in raw.get("segments", []):
        seg_words = [
            WordSegment(
                word=w["word"],
                start=w["start"],
                end=w["end"],
                confidence=w.get("confidence", 1.0),
            )
            for w in seg.get("words", [])
        ]
        words.extend(seg_words)
        segments.append(
            TranscriptSegment(
                text=seg["text"],
                start=seg["start"],
                end=seg["end"],
                words=seg_words,
            )
        )
    return TimestampedResult(
        job_id=raw.get("id", raw.get("job_id", "")),
        text=raw.get("text", ""),
        words=words,
        segments=segments,
    )
