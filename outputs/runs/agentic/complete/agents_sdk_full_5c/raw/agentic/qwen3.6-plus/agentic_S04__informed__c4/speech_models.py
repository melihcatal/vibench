"""Local request, response, and normalization helpers for Batch Speech-to-Text using AssemblyAI."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class TranscriptionRequest:
    """Normalized request payload for batch transcription."""
    audio_path: Optional[str] = None
    audio_url: Optional[str] = None
    language_code: str = "en_us"
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True
    auto_highlights: bool = False
    custom_spelling: Optional[List[dict]] = None

    def to_assemblyai_config(self) -> dict:
        """Convert to AssemblyAI TranscriptionConfig parameters."""
        config = {
            "language_code": self.language_code,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
            "auto_highlights": self.auto_highlights,
        }
        if self.speaker_labels:
            config["speaker_labels"] = True
        if self.custom_spelling:
            config["custom_spelling"] = self.custom_spelling
        return config


@dataclass
class Segment:
    """A single transcribed segment with optional metadata."""
    text: str
    speaker: Optional[str] = None
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    confidence: float = 0.0


@dataclass
class Word:
    """A single word with timing information."""
    text: str
    start_ms: int
    end_ms: int
    confidence: float = 0.0


@dataclass
class TranscriptionResponse:
    """Normalized transcription response."""
    transcript: str
    segments: List[Segment] = field(default_factory=list)
    words: List[Word] = field(default_factory=list)
    job_id: str = ""
    status: str = ""
    language: str = ""
    duration_sec: float = 0.0
    created_at: Optional[datetime] = None


def normalize_assemblyai_response(aai_result) -> TranscriptionResponse:
    """Normalize an AssemblyAI transcription result into our local model."""
    segments = []
    for utt in aai_result.utterances or []:
        segments.append(Segment(
            text=utt.text,
            speaker=f"Speaker {utt.speaker}" if utt.speaker is not None else None,
            start_ms=utt.start,
            end_ms=utt.end,
            confidence=utt.confidence,
        ))

    words = []
    for w in aai_result.words or []:
        words.append(Word(
            text=w.text,
            start_ms=w.start,
            end_ms=w.end,
            confidence=w.confidence,
        ))

    return TranscriptionResponse(
        transcript=aai_result.text or "",
        segments=segments,
        words=words,
        job_id=aai_result.id or "",
        status=aai_result.status or "",
        language=aai_result.language_code or "",
        duration_sec=(aai_result.audio_duration or 0),
    )


def extract_segments_for_translation(response: TranscriptionResponse) -> List[dict]:
    """Extract segments suitable for translation downstream processing."""
    segments = []
    for i, seg in enumerate(response.segments):
        segments.append({
            "index": i,
            "text": seg.text,
            "speaker": seg.speaker,
            "start_ms": seg.start_ms,
            "end_ms": seg.end_ms,
        })
    if not segments and response.transcript:
        segments.append({
            "index": 0,
            "text": response.transcript,
            "speaker": None,
            "start_ms": None,
            "end_ms": None,
        })
    return segments
