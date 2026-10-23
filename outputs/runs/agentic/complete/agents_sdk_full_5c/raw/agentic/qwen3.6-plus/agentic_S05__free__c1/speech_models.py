"""Define local request, response, and normalization helpers for Streaming Speech-to-Text.

Provides dataclasses and utility functions for working with Google Cloud Speech-to-Text
streaming recognition requests and responses.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from google.cloud.speech_v1p1beta1 import types as speech_types


@dataclass
class SpeechRequest:
    """Normalized request wrapper for Google Cloud Speech streaming input.

    Args:
        audio_content: Raw audio bytes for a single chunk.
        language_code: BCP-47 language code for this chunk.
        streaming: Whether this is part of a streaming session.
    """
    audio_content: bytes
    language_code: str = "en-US"
    streaming: bool = True

    def to_streaming_request(self) -> speech_types.StreamingRecognizeRequest:
        """Convert to a Google Cloud Speech StreamingRecognizeRequest."""
        return speech_types.StreamingRecognizeRequest(
            audio_content=self.audio_content,
        )


@dataclass
class WordInfo:
    """Normalized word-level information from Google Cloud Speech recognition.

    Args:
        word: The recognized word text.
        start_time: Word start time offset in milliseconds.
        end_time: Word end time offset in milliseconds.
        confidence: Confidence score for this word (0.0 to 1.0).
    """
    word: str
    start_time: float = 0.0
    end_time: float = 0.0
    confidence: float = 0.0


@dataclass
class TranscriptSegment:
    """Normalized transcript segment from a recognition result.

    Args:
        transcript: The recognized text.
        is_final: Whether this is a final (non-interim) result.
        confidence: Overall confidence score (0.0 to 1.0).
        language_code: Detected or configured language code.
        words: Optional list of word-level information.
        result_index: Index of this result in the streaming session.
    """
    transcript: str
    is_final: bool = False
    confidence: float = 0.0
    language_code: str = "en-US"
    words: List[WordInfo] = field(default_factory=list)
    result_index: int = 0

    @property
    def is_empty(self) -> bool:
        return not self.transcript.strip()

    @property
    def word_count(self) -> int:
        return len(self.words)


@dataclass
class StreamingResponse:
    """Normalized wrapper for a Google Cloud Speech streaming response.

    Args:
        segments: List of transcript segments from the response.
        raw_response: The original StreamingRecognizeResponse.
    """
    segments: List[TranscriptSegment] = field(default_factory=list)
    raw_response: Optional[Any] = None


def normalize_word_info(
    word_info: speech_types.WordInfo,
) -> WordInfo:
    """Normalize a Google Cloud Speech WordInfo to a local WordInfo dataclass.

    Args:
        word_info: WordInfo from a Google Cloud Speech alternative.

    Returns:
        Normalized WordInfo with millisecond timing.
    """
    start_ms = 0.0
    end_ms = 0.0
    if hasattr(word_info, 'start_time') and word_info.start_time is not None:
        start_ms = word_info.start_time.total_seconds() * 1000
    if hasattr(word_info, 'end_time') and word_info.end_time is not None:
        end_ms = word_info.end_time.total_seconds() * 1000

    return WordInfo(
        word=word_info.word,
        start_time=start_ms,
        end_time=end_ms,
        confidence=word_info.confidence,
    )


def normalize_recognition_result(
    result: speech_types.StreamingRecognitionResult,
    result_index: int = 0,
    language_code: str = "en-US",
) -> List[TranscriptSegment]:
    """Normalize a Google Cloud StreamingRecognitionResult to TranscriptSegments.

    Args:
        result: StreamingRecognitionResult from Google Cloud Speech API.
        result_index: Sequential index of this result.
        language_code: Language code for the result.

    Returns:
        List of normalized TranscriptSegment objects, one per alternative.
    """
    segments = []

    for alternative in result.alternatives:
        words = []
        if hasattr(alternative, 'words') and alternative.words:
            words = [normalize_word_info(w) for w in alternative.words]

        segment = TranscriptSegment(
            transcript=alternative.transcript,
            is_final=result.is_final,
            confidence=alternative.confidence,
            language_code=language_code,
            words=words,
            result_index=result_index,
        )
        segments.append(segment)

    return segments


def normalize_streaming_response(
    response: speech_types.StreamingRecognizeResponse,
    result_index_offset: int = 0,
    language_code: str = "en-US",
) -> StreamingResponse:
    """Normalize an entire Google Cloud StreamingRecognizeResponse.

    Args:
        response: StreamingRecognizeResponse from the streaming API.
        result_index_offset: Starting index for result numbering.
        language_code: Language code for results.

    Returns:
        Normalized StreamingResponse containing all segments.
    """
    all_segments = []
    for idx, result in enumerate(response.results):
        segments = normalize_recognition_result(
            result,
            result_index=result_index_offset + idx,
            language_code=language_code,
        )
        all_segments.extend(segments)

    return StreamingResponse(
        segments=all_segments,
        raw_response=response,
    )


def clean_transcript_text(text: str) -> str:
    """Clean and normalize transcript text from Google Cloud Speech output.

    Removes excessive whitespace, normalizes punctuation spacing, and strips
    leading/trailing whitespace.

    Args:
        text: Raw transcript text.

    Returns:
        Cleaned transcript text.
    """
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([.,;:!?\)])', r'\1', text)
    text = re.sub(r'([(\[])\s+', r'\1', text)
    return text
