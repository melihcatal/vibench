"""
speech_models.py - Local request, response, and normalization helpers for Batch Speech-to-Text.

Uses AssemblyAI API data structures and provides normalization utilities
for transcription payloads, responses, and speaker diarization results.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Optional, Dict, Any


# AssemblyAI-specific transcription status values
class TranscriptionStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class WordTimestamp:
    """Represents a single word with its timing information from AssemblyAI."""
    text: str
    start: int  # milliseconds
    end: int    # milliseconds
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Segment:
    """A transcript segment with speaker label and timestamps."""
    text: str
    speaker: Optional[str] = None
    start: int = 0
    end: int = 0
    words: List[WordTimestamp] = field(default_factory=list)
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["words"] = [w.to_dict() for w in self.words]
        return data


@dataclass
class TranscriptionRequest:
    """
    Request payload for submitting audio to AssemblyAI batch transcription API.
    AssemblyAI-specific fields: audio_url, speaker_labels, punctuate, format_text, etc.
    """
    audio_url: str
    model: str = "assemblyai/nano"  # AssemblyAI model identifier
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True
    language_code: str = "en"
    word_boost: Optional[List[str]] = None
    custom_spelling: Optional[List[Dict[str, List[str]]]] = None
    content_safety: bool = False
    iab_categories: bool = False

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "audio_url": self.audio_url,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
            "language_code": self.language_code,
        }
        if self.speaker_labels:
            payload["speaker_labels"] = True
        if self.word_boost:
            payload["word_boost"] = self.word_boost
        if self.custom_spelling:
            payload["custom_spelling"] = self.custom_spelling
        if self.content_safety:
            payload["content_safety"] = True
        if self.iab_categories:
            payload["iab_categories"] = True
        return payload


@dataclass
class TranscriptionResponse:
    """Normalized response from AssemblyAI batch transcription."""
    transcription_id: str
    status: TranscriptionStatus
    audio_url: str
    text: str = ""
    segments: List[Segment] = field(default_factory=list)
    words: List[WordTimestamp] = field(default_factory=list)
    confidence: float = 0.0
    audio_duration: float = 0.0
    error: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["segments"] = [s.to_dict() for s in self.segments]
        data["words"] = [w.to_dict() for w in self.words]
        return data

    @classmethod
    def from_assemblyai_response(cls, raw: Dict[str, Any], transcription_id: str) -> "TranscriptionResponse":
        """Parse raw AssemblyAI API response into normalized TranscriptionResponse."""
        status = TranscriptionStatus(raw.get("status", "error"))
        
        segments = []
        for utt in raw.get("utterances", raw.get("words", [])):
            if "speaker" in utt:
                seg = Segment(
                    text=utt.get("text", ""),
                    speaker=str(utt.get("speaker", "")),
                    start=utt.get("start", 0),
                    end=utt.get("end", 0),
                    confidence=utt.get("confidence", 0.0),
                )
                segments.append(seg)

        words = []
        for w in raw.get("words", []):
            words.append(WordTimestamp(
                text=w.get("text", ""),
                start=w.get("start", 0),
                end=w.get("end", 0),
                confidence=w.get("confidence", 0.0),
            ))

        return cls(
            transcription_id=transcription_id,
            status=status,
            audio_url=raw.get("audio_url", ""),
            text=raw.get("text", ""),
            segments=segments,
            words=words,
            confidence=raw.get("confidence", 0.0),
            audio_duration=raw.get("audio_duration", 0.0),
            error=raw.get("error"),
            raw_response=raw,
        )


@dataclass
class TranslationRequest:
    """Request to translate transcript segments."""
    segments: List[str]
    target_language: str
    source_language: str = "en"


@dataclass
class TranslationResponse:
    translated_segments: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class ModerationResult:
    """Result of content moderation on transcript text."""
    segment_index: int
    flagged: bool
    categories: Dict[str, float] = field(default_factory=dict)
    severity: str = "none"
    rationale: str = ""


@dataclass
class TranscriptSummary:
    """Summarized transcript output."""
    summary_text: str
    key_points: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    sentiment: str = "neutral"


@dataclass
class SegmentEmbedding:
    """Embedded segment for semantic retrieval."""
    segment_index: int
    text: str
    embedding: List[float]
    model: str = ""


def normalize_audio_url(local_path: str) -> str:
    """
    Normalize a local audio file path for AssemblyAI upload.
    Returns a placeholder URL; actual upload handled by client.
    """
    import os
    filename = os.path.basename(local_path)
    return f"https://api.assemblyai.com/v2/upload/{filename}"


def merge_segments(segments: List[Segment], max_words: int = 50) -> List[Segment]:
    """Merge short segments into larger ones for downstream processing."""
    if not segments:
        return []
    
    merged = []
    current_text = []
    current_start = segments[0].start
    current_end = segments[0].end
    current_speaker = segments[0].speaker

    for seg in segments:
        current_text.extend(seg.text.split())
        current_end = seg.end
        if seg.speaker != current_speaker and len(current_text) >= 5:
            merged.append(Segment(
                text=" ".join(current_text),
                speaker=current_speaker,
                start=current_start,
                end=current_end,
            ))
            current_text = seg.text.split()
            current_start = seg.start
            current_speaker = seg.speaker
        elif len(current_text) >= max_words:
            merged.append(Segment(
                text=" ".join(current_text),
                speaker=current_speaker,
                start=current_start,
                end=current_end,
            ))
            current_text = []
            current_start = seg.start
            current_speaker = seg.speaker

    if current_text:
        merged.append(Segment(
            text=" ".join(current_text),
            speaker=current_speaker,
            start=current_start,
            end=current_end,
        ))

    return merged
