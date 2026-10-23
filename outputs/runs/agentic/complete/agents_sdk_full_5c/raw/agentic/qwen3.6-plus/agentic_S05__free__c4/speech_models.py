"""Local request, response, and normalization helpers for Google Cloud Streaming Speech-to-Text."""

from dataclasses import dataclass, field
from typing import List, Optional

from google.cloud.speech_v1p1beta1.types import (
    SpeechRecognitionAlternative,
    SpeechRecognitionResult,
    WordInfo,
)


@dataclass
class WordTranscript:
    """Normalized word-level transcript from Google Cloud Speech streaming response."""

    word: str
    start_time_seconds: float
    end_time_seconds: float
    confidence: float


@dataclass
class TranscriptSegment:
    """A full or partial transcript segment from Google Cloud Speech streaming."""

    text: str
    is_final: bool
    stability: float
    words: List[WordTranscript] = field(default_factory=list)
    confidence: float = 0.0
    language_code: str = "en-US"


@dataclass
class StreamingSpeechEvent:
    """Container for a streaming speech recognition event."""

    segments: List[TranscriptSegment] = field(default_factory=list)
    raw_response: Optional[str] = None
    error: Optional[str] = None


def normalize_word_info(word_info: WordInfo) -> WordTranscript:
    """Convert a google.cloud.speech_v1p1beta1 WordInfo to a normalized WordTranscript."""
    start_seconds = word_info.start_time.total_seconds()
    end_seconds = word_info.end_time.total_seconds()
    return WordTranscript(
        word=word_info.word,
        start_time_seconds=start_seconds,
        end_time_seconds=end_seconds,
        confidence=word_info.confidence,
    )


def normalize_alternative(
    alt: SpeechRecognitionAlternative,
) -> TranscriptSegment:
    """Convert a Google Cloud SpeechRecognitionAlternative to a normalized TranscriptSegment."""
    words = [normalize_word_info(w) for w in alt.words] if alt.words else []
    return TranscriptSegment(
        text=alt.transcript,
        is_final=True,
        stability=1.0,
        words=words,
        confidence=alt.confidence,
    )


def normalize_streaming_result(
    result: SpeechRecognitionResult,
) -> TranscriptSegment:
    """Convert a Google Cloud SpeechRecognitionResult to a normalized TranscriptSegment."""
    if not result.alternatives:
        return TranscriptSegment(
            text="",
            is_final=result.is_final,
            stability=result.stability,
        )

    best_alt = result.alternatives[0]
    words = [normalize_word_info(w) for w in best_alt.words] if best_alt.words else []

    return TranscriptSegment(
        text=best_alt.transcript,
        is_final=result.is_final,
        stability=result.stability,
        words=words,
        confidence=best_alt.confidence,
    )


def merge_segments(segments: List[TranscriptSegment]) -> TranscriptSegment:
    """Merge multiple TranscriptSegments into a single combined segment.

    Used to consolidate interim results before finalization by Google Cloud Speech.
    """
    merged_text = " ".join(s.text for s in segments if s.text.strip())
    merged_words = []
    for s in segments:
        merged_words.extend(s.words)
    final_flag = any(s.is_final for s in segments)
    avg_confidence = sum(s.confidence for s in segments) / max(len(segments), 1)
    max_stability = max(s.stability for s in segments) if segments else 0.0

    return TranscriptSegment(
        text=merged_text.strip(),
        is_final=final_flag,
        stability=max_stability,
        words=merged_words,
        confidence=avg_confidence,
    )


def build_error_event(error_message: str) -> StreamingSpeechEvent:
    """Build a StreamingSpeechEvent representing an error from Google Cloud Speech streaming."""
    return StreamingSpeechEvent(error=error_message)
