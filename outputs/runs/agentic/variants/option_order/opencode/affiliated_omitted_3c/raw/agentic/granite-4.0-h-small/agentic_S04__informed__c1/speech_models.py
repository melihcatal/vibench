from typing import Dict, List


class TranscriptionConfig:
    """Local helper to normalize parameters for the transcription client."""

    def __init__(self, language: str = "en-US", model: str = "", num_speakers: int = 2):
        self.language = language
        self.model = model
        self.num_speakers = num_speakers

    def as_dict(self) -> Dict[str, Any]:
        """Convert to a flat dict for API payloads."""
        payload = {"language": self.language}
        if self.model:
            payload["model"] = self.model
        if self.num_speakers != 2:
            payload["num_speakers"] = self.num_speakers
        return payload


class TranscriptionResult:
    """Normalized representation of a completed transcription response."""

    def __init__(
        self,
        transcript: str,
        timestamps: Optional[List[Dict[str, float]]] = None,
        speakers: Optional[List[str]] = None,
    ):
        self.transcript = transcript
        self.timestamps = timestamps or []
        self.speakers = speakers or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transcript": self.transcript,
            "timestamps": self.timestamps,
            "speakers": self.speakers,
        }


def normalize_response(raw_response: Dict) -> TranscriptionResult:
    """Transform provider‑specific payload into the local standardized format."""
    # Example for AssemblyAI response shape (adjust for other providers as needed)
    transcript = raw_response.get("text", "")
    timestamps = raw_response.get("timestamps", [])
    # Strip speaker diarization if present in a separate field
    speakers = None
    if "speakers" in raw_response:
        speakers = raw_response["speakers"]
    return TranscriptionResult(
        transcript=transcript, timestamps=timestamps, speakers=speakers
    )
