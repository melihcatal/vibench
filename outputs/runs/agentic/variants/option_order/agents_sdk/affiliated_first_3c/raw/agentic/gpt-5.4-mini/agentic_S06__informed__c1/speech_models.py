from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


@dataclass
class TTSRequest:
    text: str
    voice_name: Optional[str] = None
    locale: Optional[str] = None
    output_format: str = "mp3"
    ssml: bool = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TTSRequest":
        return TTSRequest(
            text=normalize_text(self.text),
            voice_name=self.voice_name,
            locale=self.locale,
            output_format=self.output_format,
            ssml=self.ssml,
            extra=dict(self.extra),
        )


@dataclass
class TTSResponse:
    audio: bytes
    content_type: str = "audio/mpeg"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, path: str | Path) -> Path:
        out = Path(path)
        out.write_bytes(self.audio)
        return out
