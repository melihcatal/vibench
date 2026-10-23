from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _coerce_locale(value: Any, default: str = "en-US") -> str:
    text = _coerce_text(value)
    return text or default


def _normalize_voice(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return {k: v for k, v in value.items() if v is not None}
    if value is None:
        return {}
    return {"name": _coerce_text(value)}


@dataclass
class SpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: str = "en-US"
    ssml: bool = False
    output_format: str = "mp3"
    extras: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> Dict[str, Any]:
        data = {
            "text": _coerce_text(self.text),
            "locale": _coerce_locale(self.locale),
            "output_format": _coerce_text(self.output_format) or "mp3",
            "ssml": bool(self.ssml),
        }
        if self.voice:
            data["voice"] = _coerce_text(self.voice)
        if self.extras:
            data.update({k: v for k, v in self.extras.items() if v is not None})
        return data


@dataclass
class SpeechResponse:
    audio: bytes
    content_type: str = "audio/mpeg"
    voice: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_ssml(text: Any, voice: Optional[Any] = None, rate: Optional[Any] = None, pitch: Optional[Any] = None) -> str:
    body = _coerce_text(text)
    attrs = []
    if voice:
        attrs.append(f'name="{_coerce_text(voice)}"')
    speak = f"<speak><voice {' '.join(attrs)}>" if attrs else "<speak><voice>"
    prosody_attrs = []
    if rate:
        prosody_attrs.append(f'rate="{_coerce_text(rate)}"')
    if pitch:
        prosody_attrs.append(f'pitch="{_coerce_text(pitch)}"')
    if prosody_attrs:
        return f'{speak}<prosody {' '.join(prosody_attrs)}>{body}</prosody></voice></speak>'
    return f"{speak}{body}</voice></speak>"
