from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextToSpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    format: str = "mp3"

    def normalized_text(self) -> str:
        return " ".join(self.text.split())


@dataclass
class TextToSpeechResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ScriptSafetyResult:
    unsafe: bool
    provider_payload: Dict[str, Any]
    details: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingResult:
    vector: list[float]
    provider_payload: Dict[str, Any]
    model: str
