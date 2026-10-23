from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class TranscriptionConfig:
    """Configuration for a speech-to-text transcription request."""

    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    enable_speaker_diarization: bool = False
    diarization_speaker_count: Optional[int] = None
    enable_word_time_offsets: bool = False
    model: str = "default"  # or "video", "phone_call", "latest_long"


@dataclass
class TranscriptionAudio:
    """Represents the audio source for transcription."""

    uri: str  # Google Cloud Storage URI, e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac"


@dataclass
class TranscriptionRequest:
    """Combines configuration and audio for a transcription request."""

    audio: TranscriptionAudio
    config: TranscriptionConfig


@dataclass
class WordInfo:
    """Information about a transcribed word, including timestamps."""

    word: str
    start_time: float
    end_time: float
    speaker_tag: Optional[int] = None


@dataclass
class Alternative:
    """A single transcription alternative, potentially with word-level details."""

    transcript: str
    confidence: Optional[float] = None
    words: List[WordInfo] = field(default_factory=list)


@dataclass
class Result:
    """A transcription result for a segment of audio."""

    alternatives: List[Alternative]
    channel_tag: Optional[int] = None


@dataclass
class TranscriptionResponse:
    """The full response from a speech-to-text transcription."""

    results: List[Result] = field(default_factory=list)
    total_billed_time: Optional[str] = None
    uri: Optional[str] = None  # Original audio URI for reference
