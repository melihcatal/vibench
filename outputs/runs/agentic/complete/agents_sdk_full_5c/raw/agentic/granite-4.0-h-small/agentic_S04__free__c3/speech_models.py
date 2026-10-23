from typing import List, Dict, Any

BatchTranscriptionRequest = Dict[str, Any]
BatchTranscriptionResult = Dict[str, Any]

# Simple normalize function for payload construction

def normalize_transcription_payload(files: List[str], properties: Dict[str, str] = None) -> BatchTranscriptionRequest:
    """Construct a speech-to-text request payload with optional property overrides."""
    payload: BatchTranscriptionRequest = {
        "files": files,
        "properties": properties or {}
    }
    return payload

# Example: build a payload for diarization request
# payload = normalize_transcription_payload(["meeting.wav"], properties={"SpeakerDiarization": "True", "SpeakerCount": "2"})
