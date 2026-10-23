# [HELPER] speech_models.py
"""Local utilities for request/response normalization and helper functions for the batch STT workflow."""

from typing import Any, Dict, List

# ------------------------------------------------------------------------------
# Request normalization helpers
# ------------------------------------------------------------------------------
def prepare_transcription_request(audio_path: str,
                                  language: str = "en-US",
                                  diarization: bool = False,
                                  timestamping: bool = False) -> Dict[str, Any]:
    """
    Build a canonical request payload for the BatchSpeechClient.
    """
    payload = {
        "audio_path": audio_path,
        "language": language,
        "diarization": {
            "enabled": diarization,
            "speaker_count": 2   # default; callers can override
        },
        "timestamping": timestamping
    }
    return payload

# ------------------------------------------------------------------------------
# Response parsing helpers
# ------------------------------------------------------------------------------

def extract_transcript(result: Dict[str, Any]) -> List[str]:
    """
    Pull out the raw transcript strings from a Watson-like response.
    """
    transcripts = []
    for result_item in result.get("results", []):
        for alt in result_item.get("alternatives", []):
            transcripts.append(alt.get("transcript", ""))
    return transcripts


def extract_timestamps(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Flatten timestamps for words spoken in the audio.
    """
    timestamps = []
    for item in result.get("results", []):
        for alt in item.get("alternatives", []):
            for word in alt.get("timestamps", []):
                timestamps.append({
                    "word": word.get("word", ""),
                    "start": word.get("start", 0),
                    "end": word.get("end", 0)
                })
    return timestamps

# ------------------------------------------------------------------------------
# Example normalization to a uniform dict that later-step scripts can rely on
# ------------------------------------------------------------------------------

def normalize_result(raw_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert provider‑specific raw format into a generic schema:
    {
        "job_id": str,
        "status": str,
        "transcript": str,         # concatenated text or list
        "timestamps": List[Dict], # optional
        "speaker_labels": List[str] # optional
    }
    """
    return {
        "job_id": raw_result.get("job_id", "unknown"),
        "status": raw_result.get("status", "unknown"),
        "transcript": " ".join(extract_transcript(raw_result)),
        "timestamps": extract_timestamps(raw_result),
        "speaker_labels": raw_result.get("speaker_labels", [])
    }

# ------------------------------------------------------------------------------
# Export helpers for later‑step scripts
# ------------------------------------------------------------------------------
exported = {
    "prepare_transcription_request": prepare_transcription_request,
    "extract_transcript": extract_transcript,
    "extract_timestamps": extract_timestamps,
    "normalize_result": normalize_result,
}

if __name__ == "__main__":
    # Simple demo of the helpers (not part of the production build)
    demo_payload = prepare_transcription_request("/tmp/sample.wav", language="en-US", diarization=True)
    print("Demo payload:", demo_payload)
    print("Demo timestamps:", extract_timestamps({}))
