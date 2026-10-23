from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class SpeechRequest:
    text: str
    voice_name: Optional[str] = None
    locale: Optional[str] = None
    format: str = "audio/mpeg"
    prosody: Optional[Dict[str, Any]] = None
    ssml: bool = False


@dataclass
class SpeechResponse:
    audio: bytes
    provider: str
    content_type: str = "audio/mpeg"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VoiceOption:
    name: str
    locale: str
    gender: Optional[str] = None
    style: Optional[str] = None
    neural: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponse:
    text: str
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyResult:
    text: str
    provider: str
    flagged: bool
    categories: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    text: str
    provider: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptResult:
    text: str
    provider: str
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if locale is None:
        return None
    return locale.replace("_", "-").lower()


def ssml_wrap(text: str, voice_name: Optional[str] = None, prosody: Optional[Mapping[str, Any]] = None) -> str:
    attrs = ""
    if prosody:
        attrs = " ".join(f'{k}="{v}"' for k, v in prosody.items())
        attrs = f"<prosody {attrs}>{text}</prosody>"
    body = attrs or text
    if voice_name:
        return f'<speak version="1.0" xml:lang="en-US"><voice name="{voice_name}">{body}</voice></speak>'
    return f'<speak version="1.0" xml:lang="en-US">{body}</speak>'
