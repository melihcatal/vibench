from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SpeechConfig:
    provider: str
    language: str = "en-US"
    punctuation: bool = True
    api_key: Optional[str] = None
    region: Optional[str] = None
    model: Optional[str] = None


@dataclass
class StreamingTranscript:
    text: str
    is_final: bool = False
    language: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_transcript(payload: Dict[str, Any]) -> StreamingTranscript:
    text = payload.get("text") or payload.get("transcript") or payload.get("content") or ""
    is_final = bool(payload.get("final") or payload.get("is_final") or payload.get("type") == "final")
    language = payload.get("language") or payload.get("locale")
    return StreamingTranscript(text=text.strip(), is_final=is_final, language=language, raw=payload)
