from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class TTSRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    format: str = "mp3"
    ssml: bool = False
    prosody_rate: Optional[str] = None
    prosody_pitch: Optional[str] = None

    def normalized_text(self) -> str:
        value = (self.text or "").strip()
        return value

    def normalized_voice(self) -> Optional[str]:
        return self.voice.strip() if self.voice else None


@dataclass(frozen=True)
class TTSResponse:
    audio: bytes
    content_type: str = "audio/mpeg"
    provider: str = "azure"
    voice: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class VoiceSelection:
    name: str
    locale: str
    gender: Optional[str] = None
    provider: str = "azure"


def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if not locale:
        return None
    return locale.replace("_", "-").strip().lower()


def build_ssml(text: str, voice: str, rate: Optional[str] = None, pitch: Optional[str] = None, locale: Optional[str] = None) -> str:
    safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    attrs = []
    if rate:
        attrs.append(f'rate="{rate}"')
    if pitch:
        attrs.append(f'pitch="{pitch}"')
    prosody_attrs = " ".join(attrs)
    lang = normalize_locale(locale) or "en-us"
    return (
        f'<speak version="1.0" xml:lang="{lang}">'
        f'<voice name="{voice}">'
        f'<prosody {prosody_attrs}>{safe_text}</prosody>'
        f'</voice>'
        f'</speak>'
    )


def response_to_dict(response: TTSResponse) -> Mapping[str, Any]:
    return {
        "content_type": response.content_type,
        "provider": response.provider,
        "voice": response.voice,
        "metadata": response.metadata or {},
        "audio_length": len(response.audio),
    }
