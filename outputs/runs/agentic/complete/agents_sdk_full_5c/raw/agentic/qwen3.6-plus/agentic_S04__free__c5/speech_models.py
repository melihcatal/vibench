"""
Define local request, response, and normalization helpers for Batch Speech-to-Text.

Provider: AWS Transcribe (amazon.transcribe)
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class TranscriptionStatus(str, Enum):
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class LanguageCode(str, Enum):
    EN_US = "en-US"
    EN_GB = "en-GB"
    ES_US = "es-US"
    FR_FR = "fr-FR"
    DE_DE = "de-DE"
    JA_JP = "ja-JP"
    ZH_CN = "zh-CN"
    PT_BR = "pt-BR"
    HI_IN = "hi-IN"


@dataclass
class TranscriptionRequest:
    """Normalized request model for batch transcription submission."""
    job_name: str
    media_uri: str
    language_code: LanguageCode = LanguageCode.EN_US
    output_bucket_name: Optional[str] = None
    output_key_prefix: Optional[str] = None
    enable_diarization: bool = False
    max_speaker_labels: Optional[int] = None
    enable_word_timestamps: bool = True
    vocabulary_name: Optional[str] = None
    channel_id: Optional[int] = None
    tags: list[dict[str, str]] = field(default_factory=list)


@dataclass
class WordTiming:
    """Represents a single word with timing information from AWS Transcribe."""
    word: str
    start_time_ms: float
    end_time_ms: float
    confidence: float
    speaker: Optional[str] = None


@dataclass
class Segment:
    """Represents a segment of transcribed speech."""
    segment_id: str
    speaker: Optional[str]
    start_time_ms: float
    end_time_ms: float
    text: str
    word_timings: list[WordTiming]
    confidence: float


@dataclass
class TranscriptionResult:
    """Normalized response model for a completed transcription job."""
    job_name: str
    status: TranscriptionStatus
    language_code: str
    transcript_text: str
    segments: list[Segment]
    raw_response: dict[str, Any] = field(default_factory=dict)
    completed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None


def normalize_aws_transcribe_response(
    job_name: str,
    get_job_response: dict[str, Any],
    transcription_output: Optional[dict[str, Any]] = None,
) -> TranscriptionResult:
    """Normalize AWS Transcribe GetTranscriptionJob response into TranscriptionResult."""
    status_str = get_job_response.get("TranscriptionJob", {}).get("TranscriptionJobStatus", "FAILED")
    status = TranscriptionStatus(status_str)

    language_code = get_job_response.get(
        "TranscriptionJob", {}
    ).get("LanguageCode", "en-US")

    transcript_text = ""
    segments = []
    failure_reason = get_job_response.get("TranscriptionJob", {}).get("FailureReason")

    if transcription_output and status == TranscriptionStatus.COMPLETED:
        results = transcription_output.get("results", {})
        transcript_text = results.get("transcripts", [{}])[0].get("transcript", "")
        segments = _parse_segments(results)

    return TranscriptionResult(
        job_name=job_name,
        status=status,
        language_code=language_code,
        transcript_text=transcript_text,
        segments=segments,
        raw_response=get_job_response,
        completed_at=_parse_timestamp(
            get_job_response.get("TranscriptionJob", {}).get("CompletionTime")
        ),
        failure_reason=failure_reason,
    )


def _parse_segments(results: dict[str, Any]) -> list[Segment]:
    """Parse AWS Transcribe items into Segment objects."""
    items = results.get("items", [])
    speaker_items = results.get("speaker_labels", {}).get("segments", [])

    segment_id = 0
    current_words = []
    current_speaker = None
    segments = []

    for item in items:
        if item.get("type") == "punctuation":
            if current_words:
                current_words[-1].word += item.get("value", "")
            continue

        word = item.get("alternatives", [{}])[0].get("content", "")
        start_time = float(item.get("start_time", 0))
        end_time = float(item.get("end_time", 0))
        confidence = float(item.get("alternatives", [{}])[0].get("confidence", 0))

        speaker_label = None
        if current_words:
            speaker_label = current_words[-1].speaker

        word_timing = WordTiming(
            word=word,
            start_time_ms=start_time * 1000,
            end_time_ms=end_time * 1000,
            confidence=confidence,
            speaker=speaker_label,
        )
        current_words.append(word_timing)

        if item.get("type") == "pronunciation":
            pass

    if current_words:
        segments.append(
            Segment(
                segment_id=f"seg_{segment_id}",
                speaker=current_words[0].speaker,
                start_time_ms=current_words[0].start_time_ms,
                end_time_ms=current_words[-1].end_time_ms,
                text=" ".join(w.word for w in current_words),
                word_timings=current_words,
                confidence=sum(w.confidence for w in current_words) / len(current_words),
            )
        )

    return segments


def _parse_timestamp(ts: Optional[str]) -> Optional[datetime]:
    """Parse AWS ISO timestamp string to datetime."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def build_transcription_output_path(job_name: str, prefix: Optional[str] = None) -> str:
    """Build the default S3 key for AWS Transcribe output JSON."""
    base = prefix.rstrip("/") if prefix else ""
    return f"{base}/{job_name}.json" if base else f"{job_name}.json"
