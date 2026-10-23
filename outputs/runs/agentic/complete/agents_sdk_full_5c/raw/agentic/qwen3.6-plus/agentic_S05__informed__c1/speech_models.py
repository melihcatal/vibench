"""
Local request, response, and normalization helpers for Streaming Speech-to-Text.

Defines dataclasses for streaming transcription requests/responses,
transcript normalization utilities, and Deepgram-specific response parsing.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class TranscriptStatus(Enum):
    """Status of a streaming transcript result."""
    INTERIM = "interim"
    FINAL = "final"
    ERROR = "error"


@dataclass
class SpeechConfig:
    """Configuration for streaming speech recognition."""
    model: str = "nova-2"
    language: str = "en"
    sample_rate: int = 16000
    channels: int = 1
    encoding: str = "linear16"
    smart_format: bool = True
    interim_results: bool = True
    punctuate: bool = True
    profanity_filter: bool = False
    diarize: bool = False
    keywords: Optional[List[str]] = None

    def to_deepgram_options(self) -> Dict[str, Any]:
        """Convert to Deepgram streaming options dict."""
        opts = {
            "model": self.model,
            "language": self.language,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "encoding": self.encoding,
            "smart_format": self.smart_format,
            "interim_results": self.interim_results,
            "punctuate": self.punctuate,
            "profanity_filter": self.profanity_filter,
            "diarize": self.diarize,
        }
        if self.keywords:
            opts["keywords"] = self.keywords
        return opts


@dataclass
class TranscriptChunk:
    """Represents a chunk of transcribed text from streaming recognition."""
    text: str
    status: TranscriptStatus
    confidence: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0
    speaker: Optional[int] = None
    is_final: bool = False
    timestamp: float = field(default_factory=time.time)

    @property
    def duration(self) -> float:
        """Duration of this transcript chunk in seconds."""
        return self.end_time - self.start_time

    def normalize_text(self) -> str:
        """Normalize transcript text by trimming and cleaning whitespace."""
        text = self.text.strip()
        text = " ".join(text.split())
        return text


@dataclass
class StreamingTranscriptEvent:
    """Event representing a partial or final streaming recognition result."""
    transcript: str
    is_final: bool
    confidence: float = 0.0
    words: Optional[List[Dict[str, Any]]] = None
    language: Optional[str] = None
    model_used: Optional[str] = None

    def to_chunk(self) -> TranscriptChunk:
        """Convert event to a TranscriptChunk."""
        return TranscriptChunk(
            text=self.transcript,
            status=TranscriptStatus.FINAL if self.is_final else TranscriptStatus.INTERIM,
            confidence=self.confidence,
            is_final=self.is_final,
        )


@dataclass
class AudioChunk:
    """Represents an audio chunk for streaming."""
    data: bytes
    sample_rate: int = 16000
    channels: int = 1
    is_end: bool = False


def parse_deepgram_response(response: Dict[str, Any]) -> StreamingTranscriptEvent:
    """Parse a Deepgram streaming response into a normalized event.

    Args:
        response: Raw Deepgram WebSocket/SDK response dictionary.

    Returns:
        StreamingTranscriptEvent with normalized transcript data.
    """
    channel = response.get("channel", {})
    alternatives = channel.get("alternatives", [])
    
    if not alternatives:
        return StreamingTranscriptEvent(
            transcript="",
            is_final=False,
        )

    best = alternatives[0]
    transcript_text = best.get("transcript", "").strip()
    confidence = best.get("confidence", 0.0)
    words = best.get("words", [])

    metadata = response.get("metadata", {})
    model_used = metadata.get("model", None)
    request_id = metadata.get("request_id", None)

    return StreamingTranscriptEvent(
        transcript=transcript_text,
        is_final=response.get("is_final", False),
        confidence=confidence,
        words=words,
        model_used=model_used,
    )


def normalize_transcript_text(text: str) -> str:
    """Normalize transcript text by cleaning whitespace and capitalization.

    Args:
        text: Raw transcript text.

    Returns:
        Normalized transcript text.
    """
    if not text:
        return ""
    normalized = " ".join(text.split())
    return normalized


def merge_transcript_chunks(chunks: List[TranscriptChunk]) -> str:
    """Merge multiple transcript chunks into a single string.

    Args:
        chunks: List of transcript chunks to merge.

    Returns:
        Merged transcript text.
    """
    final_chunks = [c for c in chunks if c.is_final or c.status == TranscriptStatus.FINAL]
    if not final_chunks:
        final_chunks = chunks
    
    return " ".join(c.normalize_text() for c in final_chunks if c.text.strip())


def build_streaming_request_payload(
    audio_data: bytes,
    config: Optional[SpeechConfig] = None,
) -> Dict[str, Any]:
    """Build a streaming request payload for speech recognition.

    Args:
        audio_data: Raw audio bytes to transcribe.
        config: Speech configuration options.

    Returns:
        Dictionary payload suitable for streaming API request.
    """
    if config is None:
        config = SpeechConfig()

    return {
        "audio": audio_data,
        "config": config.to_deepgram_options(),
    }
