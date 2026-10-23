"""
Local request, response, and normalization helpers for Google Cloud Streaming Speech-to-Text.

Provides dataclasses and utilities for building streaming audio requests,
parsing recognition responses, and normalizing transcript output from
the google-cloud-speech provider.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from google.cloud import speech


@dataclass
class StreamingAudioChunk:
    """Represents a chunk of audio data to send for streaming recognition."""

    content: bytes
    chunk_id: int = 0
    timestamp_ms: float = 0.0

    def to_recognition_request(self) -> speech.StreamingRecognizeRequest:
        """Convert this chunk into a Google Cloud StreamingRecognizeRequest."""
        return speech.StreamingRecognizeRequest(audio_content=self.content)


@dataclass
class InterimTranscript:
    """A partial/interim transcript result from streaming recognition."""

    text: str
    confidence: float
    is_final: bool = False
    stability: float = 0.0
    alternatives: List[str] = field(default_factory=list)
    result_end_time_seconds: float = 0.0
    word_info: Optional[List[dict]] = None


@dataclass
class FinalTranscript:
    """A finalized transcript result from streaming recognition."""

    text: str
    confidence: float
    language_code: str
    alternatives: List[str] = field(default_factory=list)
    result_end_time_seconds: float = 0.0
    word_info: Optional[List[dict]] = None


def parse_streaming_response(
    response: speech.StreamingRecognizeResponse,
) -> List[InterimTranscript | FinalTranscript]:
    """
    Parse a Google Cloud StreamingRecognizeResponse into typed transcript objects.

    Extracts interim and final results from the raw protobuf response and
    normalizes them into InterimTranscript or FinalTranscript instances.
    """
    transcripts = []

    for result in response.results:
        is_final = result.is_final
        text = ""
        confidence = 0.0
        alternatives_texts = []

        for alt in result.alternatives:
            if not text:
                text = alt.transcript
                confidence = alt.confidence
            alternatives_texts.append(alt.transcript)

        # Extract word-level timing info if available
        words = []
        if result.alternatives and hasattr(result.alternatives[0], "words"):
            for w_info in result.alternatives[0].words:
                words.append(
                    {
                        "word": getattr(w_info, "word", ""),
                        "start_seconds": float(getattr(w_info, "start_time", 0)),
                        "end_seconds": float(getattr(w_info, "end_time", 0)),
                        "confidence": float(getattr(w_info, "confidence", 0.0)),
                    }
                )

        end_time = 0.0
        if hasattr(result, "result_end_time"):
            end_time = float(getattr(result, "result_end_time", 0))

        if is_final:
            transcripts.append(
                FinalTranscript(
                    text=text.strip(),
                    confidence=confidence,
                    language_code=getattr(result, "language_code", ""),
                    alternatives=alternatives_texts,
                    result_end_time_seconds=end_time,
                    word_info=words if words else None,
                )
            )
        else:
            stability = float(getattr(result, "stability", 0.0))
            transcripts.append(
                InterimTranscript(
                    text=text.strip(),
                    confidence=confidence,
                    is_final=False,
                    stability=stability,
                    alternatives=alternatives_texts,
                    result_end_time_seconds=end_time,
                    word_info=words if words else None,
                )
            )

    return transcripts


def normalize_transcript_text(text: str) -> str:
    """Normalize transcript text by cleaning whitespace and common artifacts."""
    if not text:
        return ""
    text = text.strip()
    text = " ".join(text.split())
    return text


def build_initial_streaming_request(
    streaming_config: speech.StreamingRecognitionConfig,
) -> speech.StreamingRecognizeRequest:
    """
    Build the initial StreamingRecognizeRequest containing the streaming config.

    This must be the first request sent to google.cloud.speech.StreamingRecognize.
    """
    return speech.StreamingRecognizeRequest(streaming_config=streaming_config)
