from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(slots=True)
class TTSRequest:
    text: str
    voice_id: Optional[str] = None
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    locale: Optional[str] = None

    def as_text_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": self.text,
            "model_id": self.model_id,
        }
        return payload


@dataclass(slots=True)
class TTSResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    provider: str = "ElevenLabs"
    voice_id: Optional[str] = None
    model_id: Optional[str] = None


@dataclass(slots=True)
class VoiceSelection:
    voice_id: str
    name: str
    locale: Optional[str] = None
    preview_url: Optional[str] = None
    provider: str = "ElevenLabs"


def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if not locale:
        return None
    return locale.strip().replace("_", "-").lower()


def locale_matches(locale: Optional[str], candidate: Dict[str, Any]) -> bool:
    target = normalize_locale(locale)
    if not target:
        return True

    labels = candidate.get("labels") or {}
    possible = [
        labels.get("accent"),
        labels.get("language"),
        labels.get("locale"),
        candidate.get("fine_tuning", {}).get("language"),
    ]
    normalized = [normalize_locale(v) for v in possible if isinstance(v, str) and v.strip()]
    return any(target in item or item in target for item in normalized)


def voice_from_api(data: Dict[str, Any]) -> VoiceSelection:
    labels = data.get("labels") or {}
    locale = labels.get("locale") or labels.get("language") or labels.get("accent")
    previews = data.get("preview_url") or data.get("samples", [{}])[0].get("audio_file_url") if data.get("samples") else None
    return VoiceSelection(
        voice_id=data["voice_id"],
        name=data.get("name", data["voice_id"]),
        locale=locale,
        preview_url=previews,
    )
