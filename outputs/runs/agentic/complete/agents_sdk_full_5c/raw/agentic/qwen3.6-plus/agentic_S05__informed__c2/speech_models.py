"""
Local request, response, and normalization helpers for Google Cloud Streaming Speech-to-Text.
Provides dataclasses and utility functions for handling streaming speech recognition payloads.
"""

import dataclasses
from datetime import datetime
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech


@dataclasses.dataclass
class StreamingAudioChunk:
    """Represents a chunk of audio data to be streamed."""

    audio_bytes: bytes
    timestamp: datetime = dataclasses.field(default_factory=datetime.utcnow)

    def to_streaming_audio_request(self) -> speech.StreamingRecognizeRequest:
        """Convert to a Google Cloud StreamingRecognizeRequest."""
        return speech.StreamingRecognizeRequest(audio_content=self.audio_bytes)


@dataclasses.dataclass
class StreamingAudioConfigRequest:
    """Represents an initial streaming configuration request."""

    language_code: str
    sample_rate_hertz: int
    encoding: str = "LINEAR16"
    enable_automatic_punctuation: bool = True
    interim_results: bool = True

    def to_streaming_config_request(
        self,
    ) -> speech.StreamingRecognizeRequest:
        """Convert to a Google Cloud StreamingRecognizeRequest with config."""
        from speech_client import build_streaming_config

        config = build_streaming_config(
            sample_rate_hertz=self.sample_rate_hertz,
            language_code=self.language_code,
            enable_automatic_punctuation=self.enable_automatic_punctuation,
            interim_results=self.interim_results,
        )
        return speech.StreamingRecognizeRequest(streaming_config=config)


@dataclasses.dataclass
class PartialTranscriptResult:
    """Represents a partial (interim) transcription result."""

    transcript: str
    is_final: bool = False
    confidence: float = 0.0
    language_code: str = ""
    words: list[dict] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class FinalTranscriptResult:
    """Represents a finalized transcription result."""

    transcript: str
    confidence: float = 0.0
    language_code: str = ""
    words: list[dict] = dataclasses.field(default_factory=list)
    start_time_seconds: float = 0.0
    end_time_seconds: float = 0.0


def normalize_streaming_response(
    response: speech.StreamingRecognizeResponse,
) -> list[PartialTranscriptResult]:
    """
    Normalize a Google Cloud StreamingRecognizeResponse into PartialTranscriptResult objects.

    Args:
        response: A StreamingRecognizeResponse from the Google Cloud Speech API.

    Returns:
        List of PartialTranscriptResult objects extracted from the response.
    """
    results = []
    for result in response.results:
        for alternative in result.alternatives:
            words = []
            for word_info in alternative.words:
                words.append(
                    {
                        "word": word_info.word,
                        "start_time": word_info.start_time.total_seconds(),
                        "end_time": word_info.end_time.total_seconds(),
                        "confidence": word_info.confidence,
                    }
                )
            partial = PartialTranscriptResult(
                transcript=alternative.transcript,
                is_final=result.is_final,
                confidence=alternative.confidence,
                language_code=result.language_code,
                words=words,
            )
            results.append(partial)
    return results


def extract_final_results(
    partial_results: list[PartialTranscriptResult],
) -> list[FinalTranscriptResult]:
    """
    Extract and convert finalized results from a list of partial results.

    Args:
        partial_results: List of PartialTranscriptResult objects.

    Returns:
        List of FinalTranscriptResult objects.
    """
    final_results = []
    for partial in partial_results:
        if partial.is_final:
            start_time = partial.words[0]["start_time"] if partial.words else 0.0
            end_time = partial.words[-1]["end_time"] if partial.words else 0.0
            final = FinalTranscriptResult(
                transcript=partial.transcript,
                confidence=partial.confidence,
                language_code=partial.language_code,
                words=partial.words,
                start_time_seconds=start_time,
                end_time_seconds=end_time,
            )
            final_results.append(final)
    return final_results


def concatenate_transcripts(results: list[FinalTranscriptResult]) -> str:
    """
    Concatenate transcript text from multiple final results.

    Args:
        results: List of FinalTranscriptResult objects.

    Returns:
        Concatenated transcript string with spaces between segments.
    """
    return " ".join(r.transcript for r in results if r.transcript).strip()
