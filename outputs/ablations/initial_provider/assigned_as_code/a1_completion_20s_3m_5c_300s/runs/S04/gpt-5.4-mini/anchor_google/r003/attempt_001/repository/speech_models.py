from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_segments(items: Any) -> List[Dict[str, Any]]:
    if not items:
        return []
    normalized = []
    for item in items:
        normalized.append(
            {
                "text": getattr(item, "text", None) if not isinstance(item, dict) else item.get("text"),
                "start": getattr(item, "start", None) if not isinstance(item, dict) else item.get("start"),
                "end": getattr(item, "end", None) if not isinstance(item, dict) else item.get("end"),
                "speaker": getattr(item, "speaker", None) if not isinstance(item, dict) else item.get("speaker"),
            }
        )
    return normalized


def normalize_transcript(text: Any) -> str:
    if text is None:
        return ""
    if isinstance(text, str):
        return text
    if isinstance(text, list):
        return "\n".join(str(x) for x in text)
    return str(text)


@dataclass
class TranscriptRequest:
    audio_uri: str
    language_code: str = "en-US"
    model: Optional[str] = None
    diarization: bool = False
    enable_word_time_offsets: bool = False


@dataclass
class TranscriptResponse:
    job_id: str
    status: str
    transcript: str = ""
    segments: Optional[List[Dict[str, Any]]] = None
