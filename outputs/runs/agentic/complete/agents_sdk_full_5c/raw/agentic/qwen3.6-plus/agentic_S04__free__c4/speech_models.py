"""
Define local request, response, and normalization helpers for Batch Speech-to-Text
using AssemblyAI API response structures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptWord:
    """Normalized word-level transcript entry."""
    text: str
    start: float  # milliseconds
    end: float    # milliseconds
    confidence: float
    speaker: Optional[str] = None


@dataclass
class TranscriptUtterance:
    """Normalized utterance/segment entry."""
    text: str
    speaker: Optional[str] = None
    start: float = 0.0
    end: float = 0.0
    words: List[TranscriptWord] = field(default_factory=list)


@dataclass
class TranscriptResult:
    """Full normalized transcription result."""
    job_id: str
    text: str
    confidence: float
    words: List[TranscriptWord] = field(default_factory=list)
    utterances: List[TranscriptUtterance] = field(default_factory=list)
    language_code: Optional[str] = None
    audio_duration: Optional[float] = None


def normalize_word(raw_word: Dict[str, Any]) -> TranscriptWord:
    """Convert a raw AssemblyAI word dict to a normalized TranscriptWord."""
    return TranscriptWord(
        text=raw_word.get("text", ""),
        start=float(raw_word.get("start", 0)),
        end=float(raw_word.get("end", 0)),
        confidence=float(raw_word.get("confidence", 0.0)),
        speaker=raw_word.get("speaker"),
    )


def normalize_utterance(raw_utterance: Dict[str, Any]) -> TranscriptUtterance:
    """Convert a raw AssemblyAI utterance dict to a normalized TranscriptUtterance."""
    words = [normalize_word(w) for w in raw_utterance.get("words", [])]
    return TranscriptUtterance(
        text=raw_utterance.get("text", ""),
        speaker=raw_utterance.get("speaker"),
        start=float(raw_utterance.get("start", 0)),
        end=float(raw_utterance.get("end", 0)),
        words=words,
    )


def normalize_transcription_response(raw_response: Dict[str, Any]) -> TranscriptResult:
    """
    Convert a raw AssemblyAI transcription response to a normalized TranscriptResult.
    """
    words = [normalize_word(w) for w in raw_response.get("words", [])]
    utterances_raw = raw_response.get("utterances", [])
    utterances = [normalize_utterance(u) for u in utterances_raw] if utterances_raw else []

    return TranscriptResult(
        job_id=raw_response.get("id", ""),
        text=raw_response.get("text", ""),
        confidence=float(raw_response.get("confidence", 0.0)),
        words=words,
        utterances=utterances,
        language_code=raw_response.get("language_code"),
        audio_duration=float(raw_response["audio_duration"]) if "audio_duration" in raw_response else None,
    )


def extract_segments(result: TranscriptResult) -> List[Dict[str, Any]]:
    """
    Extract transcript segments suitable for downstream processing.
    Each segment contains text, speaker, timestamps, and raw word indices.
    """
    segments = []
    for i, utt in enumerate(result.utterances):
        segments.append({
            "segment_id": i,
            "text": utt.text,
            "speaker": utt.speaker,
            "start_ms": utt.start,
            "end_ms": utt.end,
            "word_count": len(utt.words),
        })
    if not segments and result.text:
        segments.append({
            "segment_id": 0,
            "text": result.text,
            "speaker": None,
            "start_ms": 0.0,
            "end_ms": result.audio_duration or 0.0,
            "word_count": len(result.words),
        })
    return segments
