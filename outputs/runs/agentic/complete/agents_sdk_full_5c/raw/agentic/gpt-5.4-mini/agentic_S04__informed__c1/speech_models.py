from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class TranscriptionRequest:
    audio_url: str
    webhook_url: Optional[str] = None
    language_code: Optional[str] = None
    speaker_labels: bool = False
    word_boost: list[str] = field(default_factory=list)


@dataclass
class TranscriptionResult:
    job_id: str
    status: str
    text: str = ""
    confidence: Optional[float] = None
    raw: Optional[dict[str, Any]] = None


@dataclass
class TranscriptSegment:
    speaker: Optional[str]
    start_ms: Optional[int]
    end_ms: Optional[int]
    text: str
    words: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class NormalizedTranscript:
    job_id: str
    status: str
    text: str
    segments: list[TranscriptSegment] = field(default_factory=list)
    raw: Optional[dict[str, Any]] = None


def normalize_assemblyai_transcript(transcript: Any) -> NormalizedTranscript:
    segments: list[TranscriptSegment] = []
    utterances = getattr(transcript, "utterances", None) or []
    for item in utterances:
        segments.append(
            TranscriptSegment(
                speaker=getattr(item, "speaker", None),
                start_ms=getattr(item, "start", None),
                end_ms=getattr(item, "end", None),
                text=getattr(item, "text", ""),
                words=[w for w in getattr(item, "words", []) or []],
            )
        )
    return NormalizedTranscript(
        job_id=str(getattr(transcript, "id", "")),
        status=str(getattr(transcript, "status", "")),
        text=str(getattr(transcript, "text", "") or ""),
        segments=segments,
        raw=getattr(transcript, "json_response", None),
    )
