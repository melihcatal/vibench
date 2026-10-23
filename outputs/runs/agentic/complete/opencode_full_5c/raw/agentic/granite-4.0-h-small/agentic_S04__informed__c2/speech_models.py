import os
import json

# Load API key from environment
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Helper for constructing Batch-STT request payloads
REQUEST_SCHEMA = {
    "type": "object",
    "properties": {"audio_url": {"type": "string"}, "config": {"type": "object"}},
    "required": ["audio_url", "config"],
}


def normalize_timestamps(timestamps: dict) -> dict:
    """Convert timestamps dict from API format to normalized format."""
    # Example transformation - adjust keys as per actual API response
    normalized = {"words": [], "segments": []}
    for word in timestamps.get("words", []):
        normalized["words"].append(
            {
                "text": word.get("text"),
                "start": word.get("start"),
                "end": word.get("end"),
            }
        )
    for seg in timestamps.get("segments", []):
        normalized["segments"].append(
            {"text": seg.get("text"), "start": seg.get("start"), "end": seg.get("end")}
        )
    return normalized


# Example response parsing
def parse_transcript_response(resp: dict) -> dict:
    """Parse raw API response into structured transcript."""
    transcript = {
        "text": resp.get("text", ""),
        "timestamps": normalize_timestamps(resp.get("timestamps", {})),
        "speaker_labels": [],
    }
    # Extract speaker labels if speaker diarization enabled
    if resp.get("speaker_labels"):
        transcript["speaker_labels"] = [
            {"id": s.get("speaker"), "name": f"Speaker {s.get('speaker')}"}
            for s in resp.get("speaker_labels", [])
        ]
    return transcript
