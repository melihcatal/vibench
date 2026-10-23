import json
from typing import TypedDict, List

# Request structures for Batch Speech-to-Text
class BatchTranscriptionRequest(TypedDict):
    contentUrls: List[str]
    properties: Dict[str, Any]

# Minimal response structure used by helpers
class BatchTranscriptionResponse(TypedDict):
    jobId: str
    state: str

# Normalizer that extracts a clean transcript string from the full service response
def normalize_transcript(result_json: Dict[str, Any]) -> str:
    if result_json.get("state") != "Succeeded":
        raise ValueError("Transcription job not yet completed")
    transcripts = [r.get("Transcript", "") for r in result_json.get("results", [])]
    return "\n".join(transcripts)

# Export the normalized payload for later steps
__all__ = ["BatchTranscriptionRequest", "BatchTranscriptionResponse", "normalize_transcript"]
