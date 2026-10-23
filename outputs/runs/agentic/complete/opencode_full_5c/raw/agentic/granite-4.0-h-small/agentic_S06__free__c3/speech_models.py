# local helper - request, response structs and normalization utilities for Text-to-Speech

from typing import NamedTuple, List
from dataclasses import dataclass


# ---------- Request models ----------
@dataclass
class SynthesizeRequest:
    text: str
    ssml: str = ""
    voice_name: str = ""
    locale: str = "en-US"

    def to_dict(self) -> dict:
        payload = {"text": self.text}
        if self.ssml:
            payload["ssml"] = self.ssml
        if self.voice_name:
            payload["voice_name"] = self.voice_name
        payload["locale"] = self.locale
        return payload


# ---------- Response models ----------
@dataclass
class SynthesizeResponse(NamedTuple):
    audio_bytes: bytes
    duration_ms: int = 0
    voice_used: str = ""
    success: bool = False

    @staticmethod
    def from_raw(raw: dict) -> "SynthesizeResponse":
        return SynthesizeResponse(
            audio_bytes=raw.get("audio", b""),
            duration_ms=raw.get("duration_ms", 0),
            voice_used=raw.get("voice_used", ""),
            success=raw.get("success", False),
        )


# ---------- Normalization helpers ----------
def normalize_synth_response(raw: dict) -> SynthesizeResponse:
    """Convert provider-specific raw response into a consistent internal model."""
    return SynthesizeResponse.from_raw(raw)


# ---------- Locale helpers ----------
SUPPORTED_VOICES: List[str] = [
    # Example placeholder list; in real code this could be loaded from a JSON file or fetched from provider API
    "en-US-JennyNeural",
    "en-US-GuyNeural",
    "en-GB-SusanNeural",
    "fr-FR-HermineNeural",
]


def filter_voices_by_locale(voices: List[str], locale: str) -> List[str]:
    """Simple locale filter based on naming convention: <locale>-<identifier>"""
    return [v for v in voices if v.startswith(locale)]
