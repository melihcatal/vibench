from typing import List, Dict, Any, Optional

class TranscriptionJob:
    """
    Represents a simplified model for a batch transcription job.
    """
    def __init__(self, job_id: str, status: str, audio_uri: str, created_time: str):
        self.job_id = job_id
        self.status = status
        self.audio_uri = audio_uri
        self.created_time = created_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "status": self.status,
            "audio_uri": self.audio_uri,
            "created_time": self.created_time,
        }

class TranscriptionResult:
    """
    Represents a simplified model for transcription results.
    """
    def __init__(self, text: str, speaker: Optional[str] = None, words: Optional[List[Dict[str, Any]]] = None):
        self.text = text
        self.speaker = speaker
        self.words = words

    def to_dict(self) -> Dict[str, Any]:
        result = {"text": self.text}
        if self.speaker:
            result["speaker"] = self.speaker
        if self.words:
            result["words"] = self.words
        return result


def normalize_transcription_response(api_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a raw API response into a consistent transcription result format.
    """
    normalized = {
        "status": api_response.get("status", "Unknown"),
        "job_id": api_response.get("id"),
        "segments": []
    }
    for res in api_response.get("results", []):
        segment = TranscriptionResult(
            text=res.get("text", ""),
            speaker=res.get("speaker"),
            words=res.get("words")
        )
        normalized["segments"].append(segment.to_dict())
    return normalized
