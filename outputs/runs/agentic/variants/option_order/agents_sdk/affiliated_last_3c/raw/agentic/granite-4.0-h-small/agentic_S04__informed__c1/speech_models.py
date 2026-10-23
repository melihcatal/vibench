from typing import Dict, List

# Simple wrapper for request/response normalization across providers

class TranscriptionRequest:
    """
    Normalized request arguments for batch transcription.
    Provider-specific fields are mapped to generic keys.
    """
    def __init__(self, audio_path: str,
                 diarization: bool = False,
                 timestamps: bool = False,
                 language: str = "en-US") -> None:
        self.audio_path = audio_path
        self.diarization = diarization
        self.timestamps = timestamps
        self.language = language

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audio_path": self.audio_path,
            "diarization": self.diarization,
            "timestamps": self.timestamps,
            "language": self.language,
        }


class TranscriptionResponse:
    """
    Normalized successful response containing job ID and optional metadata.
    """
    def __init__(self, raw_response: Dict[str, Any]) -> None:
        self.raw = raw_response
        self.job_id = raw_response.get("job_id") or raw_response.get("id")
        # Additional provider-specific fields can be stored here
        self.extra = {k: v for k, v in raw_response.items() if k not in ["job_id", "id"]}

    def __bool__(self) -> bool:
        return self.job_id is not None


class TranscriptResult:
    """
    Normalized successful transcript data after job completion.
    """
    def __init__(self, raw_data: Dict[str, Any]) -> None:
        self.raw = raw_data
        # Generic structure: list of segments or words with optional speaker labels
        self.segments = []
        if "segments" in raw_data:
            self.segments = raw_data["segments"]
        elif "words" in raw_data:
            self.segments = [{"text": w["text"], "start": w.get("start"), "end": w.get("end"),
                               "speaker": w.get("speaker")} for w in raw_data["words"]]
        self.extra = {k: v for k, v in raw_data.items() if k != "segments"}

    def __bool__(self) -> bool:
        return bool(self.segments)

# End of file
