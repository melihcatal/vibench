from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextToSpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    format: str = "audio-16khz-32kbitrate-mono-mp3"


@dataclass
class TextToSpeechResponse:
    audio_bytes: bytes
    content_type: str
    metadata: Dict[str, Any]


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()


def build_ssml(text: str, voice: str, locale: str, rate: str = "0%", pitch: str = "0%") -> str:
    return (
        f'<speak version="1.0" xml:lang="{locale}">'
        f'<voice name="{voice}"><prosody rate="{rate}" pitch="{pitch}">{text}</prosody></voice>'
        f"</speak>"
    )
