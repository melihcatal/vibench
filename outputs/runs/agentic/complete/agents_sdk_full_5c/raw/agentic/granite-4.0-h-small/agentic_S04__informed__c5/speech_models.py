# [HELPER] speech_models.py
# Local request, response, and normalization helpers for Batch Speech-to-Text

import json
from typing import Dict, Any, List

# Helper to normalize raw transcription JSON result into a consistent structure
# Azure Speech SDK returns transcript_text directly, but for consistency we mimic a generic model

class SpeechResult:
    """Normalized transcription result model."""
    def __init__(self, transcript: str, job_id: str, duration: float, speakers: List[int] = None):
        self.transcript = transcript
        self.job_id = job_id
        self.duration = duration
        self.speakers = speakers or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transcript": self.transcript,
            "job_id": self.job_id,
            "duration_seconds": self.duration,
            "speakers": self.speakers
        }

    @classmethod
    def from_azure(cls, result: Any) -> 'SpeechResult':
        # Azure SDK returns result.transcript_text and result.metadata with .duration
        transcript = result.transcript_text if hasattr(result, "transcript_text") else result
        duration = getattr(result, "duration", None)
        # Not all calls return speaker info; default to empty list
        speakers = getattr(result, "speakers", None)
        return cls(transcript=transcript, job_id="unknown", duration=duration, speakers=speakers)

    @classmethod
    def normalize_response(cls, provider_name: str, raw_response: Any) -> 'SpeechResult':
        if provider_name.lower() == "azure":
            return cls.from_azure(raw_response)
        # Extend with additional provider-specific branches if needed
        raise NotImplementedError(f"Normalization for provider {provider_name} not implemented.")


def build_payload(audio_file: str, language: str = "en-US", diarization: bool = False, speaker_count: int = 2) -> Dict[str, Any]:
    """Creates a generic payload dict useful for invoking downstream steps (e.g., translation)."""
    return {
        "audio_file": audio_file,
        "language": language,
        "diarization": diarization,
        "speaker_count": speaker_count
    }
