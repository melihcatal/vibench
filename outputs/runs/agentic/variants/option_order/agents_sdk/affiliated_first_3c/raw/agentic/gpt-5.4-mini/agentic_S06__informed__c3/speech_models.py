from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TTSRequest:
    text: str
    locale: str = "en-US"
    voice: Optional[str] = None


@dataclass
class SSMLRequest:
    ssml: str
    locale: str = "en-US"
    voice: Optional[str] = None


@dataclass
class TTSResponse:
    audio_bytes: bytes
    content_type: str = "audio/wav"
    voice: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def make_ssml(text: str, voice: str, rate: str = "0%", pitch: str = "0%") -> str:
    clean = normalize_text(text)
    return (
        "<speak version='1.0' xml:lang='en-US'>"
        f"<voice name='{voice}'><prosody rate='{rate}' pitch='{pitch}'>{clean}</prosody></voice>"
        "</speak>"
    )
