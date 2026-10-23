from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class TTSRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_id: Optional[str] = None
    output_format: Optional[str] = None
    engine: Optional[str] = None
    locale: Optional[str] = None

    def normalized_input(self) -> str:
        if self.ssml:
            return self.ssml.strip()
        return (self.text or "").strip()


@dataclass
class TTSResponse:
    audio_bytes: bytes = b""
    content_type: str = "audio/mpeg"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VoiceSelection:
    voices: list[dict[str, Any]]
    locale: Optional[str] = None
    selected_voice_id: Optional[str] = None


def normalize_ssml(text: str, voice_id: Optional[str] = None, rate: Optional[str] = None, pitch: Optional[str] = None) -> str:
    content = text.strip()
    prosody_attrs = []
    if rate:
        prosody_attrs.append(f'rate="{rate}"')
    if pitch:
        prosody_attrs.append(f'pitch="{pitch}"')
    prosody = f"<prosody {' '.join(prosody_attrs)}>{content}</prosody>" if prosody_attrs else content
    if voice_id:
        return f'<speak><voice name="{voice_id}">{prosody}</voice></speak>'
    return f"<speak>{prosody}</speak>"


def voice_matches_locale(voice: Dict[str, Any], locale: str) -> bool:
    language_codes = voice.get("LanguageCodes") or voice.get("languageCodes") or []
    return any(str(code).lower().startswith(locale.lower()) for code in language_codes) or str(voice.get("LanguageCode", "")).lower().startswith(locale.lower())
