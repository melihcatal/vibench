from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import texttospeech


@dataclass(frozen=True)
class SynthRequest:
    text: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0


@dataclass(frozen=True)
class SynthResponse:
    audio_content: bytes
    voice_name: Optional[str] = None
    audio_encoding: str = "MP3"


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_ssml(ssml: str) -> str:
    return ssml.strip()


def voice_to_dict(voice: Any) -> Dict[str, Any]:
    return {
        "name": getattr(voice, "name", None),
        "language_codes": list(getattr(voice, "language_codes", []) or []),
        "ssml_gender": getattr(voice, "ssml_gender", None),
        "natural_sample_rate_hertz": getattr(voice, "natural_sample_rate_hertz", None),
    }


def synth_response_from_api(response: texttospeech.SynthesizeSpeechResponse, voice_name: Optional[str], encoding: texttospeech.AudioEncoding) -> SynthResponse:
    return SynthResponse(
        audio_content=response.audio_content,
        voice_name=voice_name,
        audio_encoding=encoding.name,
    )
