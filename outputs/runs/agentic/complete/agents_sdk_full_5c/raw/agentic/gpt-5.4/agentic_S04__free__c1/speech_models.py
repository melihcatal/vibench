from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptionJob:
    job_id: str
    status: str
    provider: str = "assemblyai"
    audio_url: Optional[str] = None
    text: str = ""
    utterances: List[Dict[str, Any]] = field(default_factory=list)
    words: List[Dict[str, Any]] = field(default_factory=list)
    language_code: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptSegment:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class NormalizedModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    scores: Dict[str, float]
    provider: str = "openai"


@dataclass
class SummaryResult:
    summary: str
    provider: str = "openai"
    model: str = "gpt-4o-mini"


@dataclass
class EmbeddingResult:
    vectors: List[List[float]]
    provider: str = "openai"
    model: str = "text-embedding-3-small"


@dataclass
class TranslationSegment:
    source_text: str
    translated_text: str
    target_language: str
    provider: str = "deepl"


def normalize_assemblyai_transcript(payload: Dict[str, Any]) -> TranscriptionJob:
    utterances = payload.get("utterances") or []
    words = payload.get("words") or []
    return TranscriptionJob(
        job_id=payload.get("id", ""),
        status=payload.get("status", "queued"),
        audio_url=payload.get("audio_url"),
        text=payload.get("text") or "",
        utterances=utterances,
        words=words,
        language_code=payload.get("language_code"),
        raw=payload,
    )


def extract_segments(job: TranscriptionJob, prefer_utterances: bool = True) -> List[TranscriptSegment]:
    if prefer_utterances and job.utterances:
        return [
            TranscriptSegment(
                text=item.get("text", ""),
                start_ms=item.get("start"),
                end_ms=item.get("end"),
                speaker=item.get("speaker"),
                confidence=item.get("confidence"),
            )
            for item in job.utterances
        ]
    if job.words:
        return [
            TranscriptSegment(
                text=item.get("text", ""),
                start_ms=item.get("start"),
                end_ms=item.get("end"),
                speaker=item.get("speaker"),
                confidence=item.get("confidence"),
            )
            for item in job.words
        ]
    if job.text:
        return [TranscriptSegment(text=job.text)]
    return []


def join_segment_text(segments: Iterable[TranscriptSegment]) -> str:
    return "\n".join(segment.text.strip() for segment in segments if segment.text and segment.text.strip())
