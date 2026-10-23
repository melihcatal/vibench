"""
Local request, response, and normalization helpers for Streaming Speech-to-Text.

Provides data models, normalization utilities, and conversion helpers for
interacting with the Google Cloud Speech-to-Text streaming API. Includes
transcript normalization, confidence scoring, and payload formatting.
"""

import re
import logging
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class StreamingRequestPayload:
    """Represents a streaming speech recognition request payload."""
    audio_bytes: bytes = b""
    is_config_request: bool = False
    language_code: str = "en-US"
    sample_rate_hertz: int = 16000
    model: str = "latest_long"
    enable_automatic_punctuation: bool = True
    enable_word_time_offsets: bool = True
    profanity_filter: bool = False
    alternative_language_codes: List[str] = field(default_factory=list)


@dataclass
class StreamingResponsePayload:
    """Represents a normalized streaming speech recognition response."""
    text: str = ""
    is_final: bool = False
    confidence: float = 0.0
    stability: float = 0.0
    result_index: int = 0
    language_code: str = "en-US"
    words: List[dict] = field(default_factory=list)
    alternatives: List[dict] = field(default_factory=list)
    raw_response: Optional[dict] = field(default=None, repr=False)


@dataclass
class TranscriptSegment:
    """A segment of transcribed speech with timing and metadata."""
    text: str
    start_time_ms: int = 0
    end_time_ms: int = 0
    confidence: float = 0.0
    speaker_id: Optional[str] = None
    language_code: str = "en-US"


def normalize_transcript(text: str) -> str:
    """
    Normalize transcript text from Google Cloud Speech-to-Text.

    Cleans up common artifacts such as multiple spaces, stray punctuation,
    and leading/trailing whitespace.
    """
    if not text:
        return ""
    normalized = text.strip()
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"\s+([,.!?;:])", r"\1", normalized)
    normalized = normalized.capitalize()
    return normalized


def compute_weighted_confidence(alternatives: List[dict]) -> float:
    """
    Compute a weighted confidence score from multiple alternatives.

    The primary (top) alternative receives higher weight in the average.
    """
    if not alternatives:
        return 0.0

    total_weight = 0.0
    weighted_sum = 0.0

    for i, alt in enumerate(alternatives):
        weight = 1.0 / (i + 1)
        confidence = alt.get("confidence", 0.0)
        weighted_sum += confidence * weight
        total_weight += weight

    if total_weight == 0:
        return 0.0

    return weighted_sum / total_weight


def response_to_payload(response: dict) -> StreamingResponsePayload:
    """
    Convert a raw Google Cloud Speech-to-Text response dict to a normalized payload.

    Args:
        response: Raw dict from the streaming API response.

    Returns:
        Normalized StreamingResponsePayload.
    """
    alternatives = response.get("alternatives", [])
    best_alt = alternatives[0] if alternatives else {}

    words = []
    for word_info in best_alt.get("words", []):
        words.append({
            "word": word_info.get("word", ""),
            "start_time_ms": word_info.get("start_time_ms", 0),
            "end_time_ms": word_info.get("end_time_ms", 0),
            "confidence": word_info.get("confidence", 0.0),
        })

    return StreamingResponsePayload(
        text=normalize_transcript(best_alt.get("transcript", "")),
        is_final=response.get("is_final", False),
        confidence=best_alt.get("confidence", 0.0),
        stability=response.get("stability", 0.0),
        result_index=response.get("result_index", 0),
        language_code=response.get("language_code", "en-US"),
        words=words,
        alternatives=alternatives,
        raw_response=response,
    )


def build_request_payload(
    audio_bytes: bytes,
    is_first: bool = False,
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    model: str = "latest_long",
) -> StreamingRequestPayload:
    """
    Build a request payload for Google Cloud Speech-to-Text streaming API.

    Args:
        audio_bytes: Raw audio chunk data.
        is_first: Whether this is the initial config request.
        language_code: BCP-47 language code.
        sample_rate_hertz: Audio sample rate.
        model: Google Cloud Speech model identifier.

    Returns:
        Configured StreamingRequestPayload.
    """
    return StreamingRequestPayload(
        audio_bytes=audio_bytes,
        is_config_request=is_first,
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
        model=model,
    )


def merge_transcript_segments(segments: List[TranscriptSegment]) -> str:
    """
    Merge a list of transcript segments into a single coherent transcript string.
    """
    if not segments:
        return ""

    sorted_segments = sorted(segments, key=lambda s: s.start_time_ms)
    parts = [s.text for s in sorted_segments if s.text]
    return " ".join(parts).strip()


def extract_keywords_from_transcript(text: str, min_word_length: int = 4) -> List[str]:
    """
    Extract potential keywords from a transcript.

    Filters out short words and common stop words.
    """
    stop_words = {
        "the", "and", "for", "are", "but", "not", "you", "all",
        "can", "had", "her", "was", "one", "our", "out", "has",
        "have", "been", "from", "this", "that", "with", "will",
        "each", "make", "like", "just", "over", "such", "more",
    }

    words = re.findall(r"\b[a-zA-Z]{%d,}\b" % min_word_length, text.lower())
    keywords = [w for w in words if w not in stop_words]
    return list(dict.fromkeys(keywords))
