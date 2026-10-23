# [HELPER] speech_models.py
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class TranscriptionConfiguration:
    """Configuration payload for batch transcription requests.
    This maps directly to the Azure Batch API request schema.
    """

    language: str = "en-US"
    diarization_enabled: bool = False
    diarization_max_speakers: int = 5


@dataclass
class TranscriptionJobResult:
    """Normalized result of a transcription job.
    Contains job metadata, error info, and the audio segments.
    """

    job_id: str
    state: str
    created_time: str
    last_modified_time: str
    error: Optional[Dict[str, str]] = None
    segments: Optional[List[Dict[str, Any]]] = None
    timestamps: Optional[List[Dict[str, str]]] = None

    def success(self) -> bool:
        return self.state == "Succeeded" and not self.error


@dataclass
class TimestampedWord:
    """Word-level timestamp information.
    Extracted from the Azure result payload and normalized for uniformity.
    """

    start: str  # ISO-like string (e.g., '00:00:01.250')
    duration: str
    text: str
    speaker_label: Optional[str] = None


@dataclass
class TranscriptionRequest:
    """Request data passed to the client.
    Keeps a reference to the provider (Azure) to make the integration explicit.
    """

    provider: str = "AzureCognitiveServices"
    audio_stream: Optional[bytes] = None
    language: str = "en-US"
    diarization_enabled: bool = False
    diarization_max_speakers: int = 5
