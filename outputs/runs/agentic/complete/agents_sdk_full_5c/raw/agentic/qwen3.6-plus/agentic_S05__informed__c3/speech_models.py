"""
Local request, response, and normalization helpers for Google Cloud Speech-to-Text streaming.

Provides dataclasses and utilities for normalizing streaming speech recognition responses
from Google Cloud Speech-to-Text API.

Provider: Google Cloud Speech-to-Text
SDK: google-cloud-speech
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

from google.cloud.speech_v1p1beta1 import types as speech_types


@dataclass
class StreamingTranscriptSegment:
    """Represents a single transcript segment from streaming recognition."""

    text: str
    confidence: float
    is_final: bool
    language_code: str = "en-US"
    alternatives: list[dict] = field(default_factory=list)
    word_timestamps: list[dict] = field(default_factory=list)


@dataclass
class StreamingTranscriptResult:
    """Aggregated result from a streaming recognition session."""

    result_id: int
    is_final: bool
    language_code: str = "en-US"
    stability: float = 0.0
    segments: list[StreamingTranscriptSegment] = field(default_factory=list)
    raw_response: Optional[dict] = field(default=None, repr=False)


def normalize_streaming_response(
    response: speech_types.StreamingRecognizeResponse,
) -> list[StreamingTranscriptResult]:
    """
    Normalize a Google Cloud Speech StreamingRecognizeResponse into local result objects.

    Args:
        response: Raw StreamingRecognizeResponse from Google Cloud Speech API.

    Returns:
        List of normalized StreamingTranscriptResult objects.
    """
    results = []
    for result in response.results:
        normalized = StreamingTranscriptResult(
            result_id=result.result_index,
            is_final=result.is_final,
            language_code="",
            stability=result.stability,
            segments=[],
            raw_response={
                "result_index": result.result_index,
                "is_final": result.is_final,
                "stability": result.stability,
            },
        )

        for alternative in result.alternatives:
            segment = StreamingTranscriptSegment(
                text=alternative.transcript,
                confidence=alternative.confidence,
                is_final=result.is_final,
            )
            normalized.segments.append(segment)

        results.append(normalized)

    return results


def extract_interim_transcript(
    response: speech_types.StreamingRecognizeResponse,
) -> Optional[str]:
    """
    Extract interim (partial) transcript text from a streaming response.

    Args:
        response: Raw StreamingRecognizeResponse.

    Returns:
        Interim transcript string or None if no interim result.
    """
    for result in response.results:
        if not result.is_final and result.alternatives:
            return result.alternatives[0].transcript
    return None


def extract_final_transcripts(
    response: speech_types.StreamingRecognizeResponse,
) -> list[str]:
    """
    Extract all final transcript texts from a streaming response.

    Args:
        response: Raw StreamingRecognizeResponse.

    Returns:
        List of final transcript strings.
    """
    transcripts = []
    for result in response.results:
        if result.is_final and result.alternatives:
            transcripts.append(result.alternatives[0].transcript)
    return transcripts


def aggregate_final_text(
    all_results: list[StreamingTranscriptResult],
) -> str:
    """
    Aggregate all final transcript segments into a single text block.

    Args:
        all_results: List of normalized streaming results.

    Returns:
        Concatenated final transcript text.
    """
    parts = []
    for r in all_results:
        if r.is_final:
            for seg in r.segments:
                parts.append(seg.text)
    return " ".join(parts).strip()


def build_error_response(error_message: str, error_code: Optional[int] = None) -> dict:
    """
    Build a standardized error response dict for streaming failures.

    Args:
        error_message: Human-readable error description.
        error_code: Optional numeric error code.

    Returns:
        Error response dictionary.
    """
    return {
        "error": error_message,
        "error_code": error_code,
        "timestamp": time.time(),
        "status": "error",
    }
