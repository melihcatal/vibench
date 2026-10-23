from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class BatchStatus(str, Enum):
    VALIDATING = "validating"
    IN_PROGRESS = "in_progress"
    FINALIZING = "finalizing"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"


class TranscriptFormat(str, Enum):
    JSON = "verbose_json"
    TEXT = "text"
    SRT = "srt"
    VTT = "vtt"


@dataclass
class AudioTranscriptionRequest:
    file_path: str
    model: str = "whisper-1"
    language: Optional[str] = None
    prompt: Optional[str] = None
    response_format: str = "verbose_json"
    temperature: float = 0.0
    timestamp_granularities: list = field(default_factory=lambda: ["word", "segment"])


@dataclass
class BatchJobRequest:
    input_file_id: str
    endpoint: str = "/v1/audio/transcriptions"
    completion_window: str = "24h"


@dataclass
class TranscriptSegment:
    id: int
    start: float
    end: float
    text: str
    tokens: list = field(default_factory=list)
    speaker: Optional[str] = None
    temperature: float = 0.0
    avg_logprob: float = 0.0
    compression_ratio: float = 0.0
    no_speech_prob: float = 0.0


@dataclass
class WordTimestamp:
    word: str
    start: float
    end: float


@dataclass
class TranscriptionResult:
    text: str
    language: str
    duration: float
    segments: list = field(default_factory=list)
    words: list = field(default_factory=list)
    job_id: Optional[str] = None
    batch_id: Optional[str] = None


@dataclass
class DiarizedSegment:
    start: float
    end: float
    text: str
    speaker: str
    confidence: float = 1.0


@dataclass
class TimestampedSegment:
    start: float
    end: float
    text: str
    words: list = field(default_factory=list)


@dataclass
class TranslatedSegment:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    segment_id: int


@dataclass
class ModerationResult:
    text: str
    flagged: bool
    categories: dict = field(default_factory=dict)
    category_scores: dict = field(default_factory=dict)
    segment_id: Optional[int] = None


@dataclass
class ArchiveSummary:
    transcript_id: str
    summary: str
    key_topics: list = field(default_factory=list)
    speaker_count: int = 0
    duration_seconds: float = 0.0
    language: str = ""
    word_count: int = 0


@dataclass
class SegmentEmbedding:
    segment_id: int
    text: str
    embedding: list = field(default_factory=list)
    model: str = "text-embedding-3-small"
    dimensions: int = 1536


@dataclass
class BatchJobStatus:
    job_id: str
    status: BatchStatus
    input_file_id: str
    output_file_id: Optional[str] = None
    error_file_id: Optional[str] = None
    created_at: int = 0
    completed_at: Optional[int] = None
    total_requests: int = 0
    completed_requests: int = 0
    failed_requests: int = 0


def normalize_transcription_response(raw_response: dict) -> TranscriptionResult:
    segments = []
    for seg in raw_response.get("segments", []):
        segments.append(
            TranscriptSegment(
                id=seg.get("id", 0),
                start=seg.get("start", 0.0),
                end=seg.get("end", 0.0),
                text=seg.get("text", "").strip(),
                tokens=seg.get("tokens", []),
                temperature=seg.get("temperature", 0.0),
                avg_logprob=seg.get("avg_logprob", 0.0),
                compression_ratio=seg.get("compression_ratio", 0.0),
                no_speech_prob=seg.get("no_speech_prob", 0.0),
            )
        )

    words = []
    for w in raw_response.get("words", []):
        words.append(
            WordTimestamp(
                word=w.get("word", ""),
                start=w.get("start", 0.0),
                end=w.get("end", 0.0),
            )
        )

    return TranscriptionResult(
        text=raw_response.get("text", ""),
        language=raw_response.get("language", ""),
        duration=raw_response.get("duration", 0.0),
        segments=segments,
        words=words,
    )


def build_diarized_segments(segments: list, speaker_assignments: dict) -> list:
    diarized = []
    for seg in segments:
        speaker_id = speaker_assignments.get(seg.id, "speaker_0")
        diarized.append(
            DiarizedSegment(
                start=seg.start if hasattr(seg, "start") else seg.get("start", 0.0),
                end=seg.end if hasattr(seg, "end") else seg.get("end", 0.0),
                text=seg.text if hasattr(seg, "text") else seg.get("text", ""),
                speaker=speaker_id,
                confidence=speaker_assignments.get(f"{seg.id}_confidence", 1.0)
                if isinstance(speaker_assignments, dict)
                else 1.0,
            )
        )
    return diarized


def build_timestamped_segments(segments: list, words: list) -> list:
    timestamped = []
    for seg in segments:
        seg_start = seg.start if hasattr(seg, "start") else seg.get("start", 0.0)
        seg_end = seg.end if hasattr(seg, "end") else seg.get("end", 0.0)
        seg_text = seg.text if hasattr(seg, "text") else seg.get("text", "")
        seg_words = (
            [w for w in words if seg_start <= w.start < seg_end] if words else []
        )
        timestamped.append(
            TimestampedSegment(
                start=seg_start,
                end=seg_end,
                text=seg_text,
                words=seg_words,
            )
        )
    return timestamped
