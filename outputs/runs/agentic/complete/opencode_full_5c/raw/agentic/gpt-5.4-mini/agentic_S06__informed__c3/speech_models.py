from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en-US").replace("_", "-")


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


@dataclass
class SpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    rate: Optional[str] = None
    pitch: Optional[str] = None
    ssml: bool = False


@dataclass
class SpeechResponse:
    audio: bytes
    content_type: str
    metadata: Dict[str, Any]


def response_from_audio(
    audio: bytes, content_type: str, **metadata: Any
) -> SpeechResponse:
    return SpeechResponse(audio=audio, content_type=content_type, metadata=metadata)


def voice_candidates(
    voices: List[Dict[str, Any]], locale: Optional[str] = None
) -> List[Dict[str, Any]]:
    target = normalize_locale(locale).lower()
    return [
        v
        for v in voices
        if target in str(v.get("locale", "")).lower()
        or target in str(v.get("localeName", "")).lower()
    ]
