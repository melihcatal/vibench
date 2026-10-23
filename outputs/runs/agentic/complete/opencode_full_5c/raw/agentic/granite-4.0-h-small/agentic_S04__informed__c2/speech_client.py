import os
import json

# Local configuration
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Helper for constructing Batch-STT request payloads
REQUEST_SCHEMA = {
    "type": "object",
    "properties": {"audio_url": {"type": "string"}, "config": {"type": "object"}},
    "required": ["audio_url", "config"],
}


def build_submit_request(audio_path: str) -> dict:
    """Normalize audio path to a URL or file URI and build request payload."""
    if audio_path.startswith("http"):
        url = audio_path
    else:
        # Simple conversion to file URI for local files
        file_uri = f"file://{os.path.abspath(audio_path)}"
        url = file_uri
    return {
        "audio_url": url,
        "config": {"speaker_diarization": False, "timestamps": "words"},
    }


# Example usage: payload = build_submit_request('/local/file.wav')
