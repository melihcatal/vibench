from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _get(payload: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in payload:
            return payload[key]
    return default


def normalize_segments(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    segments = _get(payload, "segments", "results", default=[]) or []
    normalized = []
    for segment in segments:
        normalized.append(
            {
                "start": segment.get("start"),
                "end": segment.get("end"),
                "speaker": segment.get("speaker"),
                "text": segment.get("text", ""),
            }
        )
    return normalized


def normalize_transcript(payload: Dict[str, Any]) -> str:
    if isinstance(payload, str):
        return payload
    if "transcript" in payload and isinstance(payload["transcript"], str):
        return payload["transcript"]
    segments = normalize_segments(payload)
    return " ".join(segment["text"] for segment in segments if segment["text"])


@dataclass
class TranscriptRequest:
    audio_uri: str
    language_code: str
    enable_diarization: bool = False
    enable_word_time_offsets: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audio_uri": self.audio_uri,
            "language_code": self.language_code,
            "enable_diarization": self.enable_diarization,
            "enable_word_time_offsets": self.enable_word_time_offsets,
        }


@dataclass
class TranscriptResponse:
    job_id: str
    status: str
    transcript: Optional[str] = None
    segments: Optional[List[Dict[str, Any]]] = None
