from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en-US").replace("_", "-").strip()
    parts = value.split("-")
    if len(parts) == 1:
        return parts[0].lower()
    return (
        parts[0].lower()
        + "-"
        + "-".join(part.upper() if len(part) == 2 else part for part in parts[1:])
    )


def normalize_text(text: str) -> str:
    return " ".join((text or "").split()).strip()


@dataclass
class SpeechRequest:
    text: str
    locale: str = "en-US"
    voice_name: Optional[str] = None
    output_format: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        return {
            "text": normalize_text(self.text),
            "locale": normalize_locale(self.locale),
            "voice_name": self.voice_name,
            "output_format": self.output_format,
        }


@dataclass
class SpeechResponse:
    audio: bytes
    content_type: str = "audio/mpeg"
    voice_name: Optional[str] = None
