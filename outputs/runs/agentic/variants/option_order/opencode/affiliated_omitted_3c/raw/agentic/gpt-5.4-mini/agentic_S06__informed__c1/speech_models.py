from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def normalize_ssml(ssml: str) -> str:
    return (ssml or "").strip()


@dataclass
class SpeechRequest:
    text: str
    voice_name: Optional[str] = None
    locale: Optional[str] = None
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    ssml: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": normalize_text(self.text),
            "voice_name": self.voice_name,
            "locale": self.locale,
            "speaking_rate": self.speaking_rate,
            "pitch": self.pitch,
            "ssml": normalize_ssml(self.ssml) if self.ssml is not None else None,
        }
        return {k: v for k, v in payload.items() if v is not None}


@dataclass
class SpeechResponse:
    audio_content: bytes
    voice_name: Optional[str] = None
    locale: Optional[str] = None
    mime_type: str = "audio/mpeg"
