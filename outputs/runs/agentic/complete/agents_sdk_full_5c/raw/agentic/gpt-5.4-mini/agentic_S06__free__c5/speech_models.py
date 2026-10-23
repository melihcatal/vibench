from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class TextToSpeechRequest:
    text: str
    locale: str
    voice_name: str


@dataclass(frozen=True)
class SSMLRequest:
    ssml: str
    locale: str
    voice_name: str


@dataclass(frozen=True)
class VoiceSummary:
    name: str
    locales: List[str]
    gender: str


@dataclass(frozen=True)
class VoiceSelection:
    name: str
    locale: str


@dataclass(frozen=True)
class AudioTarget:
    path: str



def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()



def normalize_ssml(ssml: str) -> str:
    ssml = ssml.strip()
    if not ssml.startswith("<speak"):
        raise ValueError("SSML must begin with <speak>")
    return ssml
