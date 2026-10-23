from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SpeechRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    locale: Optional[str] = None
    voice: Optional[str] = None
    output_format: Optional[str] = None
    prosody_rate: Optional[str] = None
    prosody_pitch: Optional[str] = None


@dataclass
class SpeechResponse:
    audio: bytes
    voice: Optional[str] = None
    format: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en-US").replace("_", "-")


def normalize_voice(
    voice: Optional[str], locale: Optional[str] = None
) -> Optional[str]:
    if voice:
        return voice.strip()
    if locale:
        return f"{normalize_locale(locale)}-Neural"
    return None


def build_ssml(
    text: str,
    voice: str,
    locale: str,
    rate: Optional[str] = None,
    pitch: Optional[str] = None,
) -> str:
    prosody = []
    if rate:
        prosody.append(f'rate="{rate}"')
    if pitch:
        prosody.append(f'pitch="{pitch}"')
    prosody_attr = f" {' '.join(prosody)}" if prosody else ""
    return f'<speak version="1.0" xml:lang="{normalize_locale(locale)}"><voice name="{voice}"><prosody{prosody_attr}>{text}</prosody></voice></speak>'
