"""Local request, response, and normalization helpers for Google Cloud Streaming Speech-to-Text."""

from dataclasses import dataclass, field
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech


@dataclass
class StreamingAudioRequest:
    """Normalized request wrapper for streaming audio chunks.

    Compatible with Google Cloud Speech-to-Text StreamingRecognizeRequest.
    """
    audio_content: bytes = b""
    is_config: bool = False
    streaming_config: Optional[speech.StreamingRecognitionConfig] = None

    def to_protobuf(self) -> speech.StreamingRecognizeRequest:
        """Convert to Google Cloud Speech-to-Text StreamingRecognizeRequest."""
        if self.is_config and self.streaming_config:
            return speech.StreamingRecognizeRequest(
                streaming_config=self.streaming_config
            )
        return speech.StreamingRecognizeRequest(
            audio_content=self.audio_content
        )


@dataclass
class StreamingTranscriptResult:
    """Normalized response wrapper for streaming transcription results.

    Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
    """
    transcript: str = ""
    is_final: bool = False
    confidence: float = 0.0
    stability: float = 0.0
    language_code: str = ""
    start_time_seconds: float = 0.0
    end_time_seconds: float = 0.0
    words: list[dict] = field(default_factory=list)

    @classmethod
    def from_google_result(
        cls, result: speech.StreamingRecognitionResult
    ) -> "StreamingTranscriptResult":
        """Parse a Google Cloud StreamingRecognitionResult into normalized form."""
        transcript = ""
        confidence = 0.0
        words = []
        start_time = 0.0
        end_time = 0.0

        if result.alternatives:
            alt = result.alternatives[0]
            transcript = alt.transcript
            confidence = alt.confidence
            start_time = (
                alt.words[0].start_time.total_seconds() if alt.words else 0.0
            )
            end_time = (
                alt.words[-1].end_time.total_seconds() if alt.words else 0.0
            )
            words = [
                {
                    "word": w.word,
                    "start_time": w.start_time.total_seconds(),
                    "end_time": w.end_time.total_seconds(),
                    "confidence": w.confidence,
                }
                for w in alt.words
            ]

        return cls(
            transcript=transcript,
            is_final=result.is_final,
            confidence=confidence,
            stability=result.stability,
            words=words,
            start_time_seconds=start_time,
            end_time_seconds=end_time,
        )


@dataclass
class StreamingResponseBatch:
    """Batch of streaming results from Google Cloud Speech-to-Text."""
    results: list[StreamingTranscriptResult] = field(default_factory=list)
    result_index: int = 0

    @classmethod
    def from_google_response(
        cls, response: speech.StreamingRecognizeResponse
    ) -> "StreamingResponseBatch":
        """Parse a Google Cloud StreamingRecognizeResponse."""
        results = [
            StreamingTranscriptResult.from_google_result(r)
            for r in response.results
        ]
        return cls(
            results=results,
            result_index=response.result_index if hasattr(response, "result_index") else 0,
        )


def normalize_transcript_text(transcript: str) -> str:
    """Normalize transcript text from Google Cloud Speech-to-Text output."""
    if not transcript:
        return ""
    text = transcript.strip()
    text = text.replace("  ", " ")
    return text


def filter_final_results(
    batch: StreamingResponseBatch,
) -> list[StreamingTranscriptResult]:
    """Filter only final results from a response batch."""
    return [r for r in batch.results if r.is_final]


def filter_interim_results(
    batch: StreamingResponseBatch,
) -> list[StreamingTranscriptResult]:
    """Filter only interim (non-final) results from a response batch."""
    return [r for r in batch.results if not r.is_final]
