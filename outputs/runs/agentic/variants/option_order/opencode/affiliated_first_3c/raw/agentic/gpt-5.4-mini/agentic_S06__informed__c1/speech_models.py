from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en-US").replace("_", "-")


@dataclass
class SpeechRequest:
    text: str
    locale: str = "en-US"
    voice: Optional[str] = None
    output_format: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        return {
            "text": normalize_text(self.text),
            "locale": normalize_locale(self.locale),
            "voice": self.voice,
            "output_format": self.output_format,
        }


@dataclass
class SpeechResponse:
    audio: bytes
    content_type: str = "audio/wav"
    voice: Optional[str] = None
