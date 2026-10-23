from dataclasses import dataclass
from typing import Any


@dataclass
class SynthesisRequest:
    text: str
    voice: str | None = None
    audio_format: str | None = None
    model: str | None = None


@dataclass
class SynthesisResponse:
    audio_bytes: bytes
    voice: str
    audio_format: str


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_ssml(ssml: str) -> str:
    return ssml.strip()


def response_bytes(response: Any) -> bytes:
    if hasattr(response, "read"):
        return response.read()
    if isinstance(response, (bytes, bytearray)):
        return bytes(response)
    return bytes(response)
