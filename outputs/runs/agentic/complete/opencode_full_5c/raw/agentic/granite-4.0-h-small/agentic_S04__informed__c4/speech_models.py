import os
import json


# Local helper: request/response models and normalization for Batch Speech-to-Text
class BatchRequest:
    """Base class for batch request payloads."""

    def to_dict(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class BatchTranscriptionRequest(BatchRequest):
    def __init__(self, audio, content_type, model, diarization=None):
        self.audio = audio
        self.content_type = content_type
        self.model = model
        self.diarization = diarization


class BatchResponse:
    """Normalized response from the provider (example fields)."""

    def __init__(self, job_id, status, transcript=None, timestamps=None):
        self.job_id = job_id
        self.status = status
        self.transcript = transcript
        self.timestamps = timestamps


class DiarizationConfig:
    def __init__(self, enabled=False, speaker_count=2):
        self.enabled = enabled
        self.speaker_count = speaker_count


# Helper utilities
def normalize_timestamps(raw_timestamps):
    """Convert provider-specific timestamp format to a standard list of dicts."""
    # Example: provider returns [{'start':0.1,'end':0.3,'word':'hello'}, ...]
    return [
        {
            "word": item.get("word"),
            "start": item.get("start"),
            "end": item.get("end"),
        }
        for item in raw_timestamps
    ]
