from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TranscriptionConfig:
    """Configuration for a speech transcription job."""

    audio_uri: str
    language_code: str = "en-US"
    enable_speaker_diarization: bool = False
    enable_word_time_offsets: bool = False
    sample_rate_hertz: Optional[int] = None


@dataclass
class TranscriptionResult:
    """Result of a speech transcription job."""

    job_name: str
    status: str
    transcript: Optional[str] = None
    word_timestamps: Optional[List[dict]] = field(default_factory=list)
    diarization_speakers: Optional[List[dict]] = field(default_factory=list)
