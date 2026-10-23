from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import texttospeech


@dataclass
class TextRequest:
    text: str
    language_code: str
    voice_name: Optional[str] = None


@dataclass
class SSMLRequest:
    ssml: str
    language_code: str
    voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0


@dataclass
class VoiceSelection:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None


@dataclass
class AudioResponse:
    audio_content: bytes
    encoding: str
    mime_type: str = "audio/mpeg"


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def build_text_input(text: str) -> texttospeech.SynthesisInput:
    return texttospeech.SynthesisInput(text=normalize_whitespace(text))


def build_ssml_input(ssml: str) -> texttospeech.SynthesisInput:
    return texttospeech.SynthesisInput(ssml=ssml.strip())


def response_to_dict(response: Any) -> Dict[str, Any]:
    return {
        "audio_content": getattr(response, "audio_content", b""),
    }
