"""Define local request, response, and normalization helpers for Text-to-Speech."""

import base64
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TTSRequest:
    """Normalized request payload for text-to-speech synthesis."""
    text: str
    voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SSMLRequest:
    """Normalized request payload for SSML-based synthesis."""
    ssml: str
    voice_id: str = "EXAVITQu4vr4xnSDxMaL"
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VoiceOption:
    """Normalized voice listing result."""
    voice_id: str
    name: str
    accent: str = ""
    description: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    preview_url: Optional[str] = None


@dataclass
class TTSResponse:
    """Normalized response after synthesis."""
    audio_bytes: bytes
    content_type: str
    voice_id: str
    model_id: str
    duration_ms: Optional[int] = None
    character_count: Optional[int] = None


def normalize_voices(raw_voices: List[Dict[str, Any]]) -> List[VoiceOption]:
    """Normalize a list of ElevenLabs voice dicts into VoiceOption objects."""
    results = []
    for v in raw_voices:
        results.append(VoiceOption(
            voice_id=v.get("voice_id", ""),
            name=v.get("name", ""),
            accent=v.get("accent", ""),
            description=v.get("description", ""),
            labels=v.get("labels", {}),
            preview_url=v.get("preview_url"),
        ))
    return results


def filter_voices_by_locale(voices: List[VoiceOption], locale: str) -> List[VoiceOption]:
    """Filter voices that match a given locale string (e.g. 'en', 'en-US', 'es')."""
    locale_lower = locale.lower().replace("-", "").replace("_", "")
    matched = []
    for v in voices:
        accent = (v.accent or "").lower().replace("-", "").replace("_", "")
        labels_str = " ".join(str(val).lower() for val in v.labels.values()).replace("-", "").replace("_", "")
        name_lower = (v.name or "").lower().replace("-", "").replace("_", "")
        if locale_lower in accent or locale_lower in labels_str or locale_lower in name_lower:
            matched.append(v)
    return matched


def build_audio_metadata(response: TTSResponse) -> Dict[str, Any]:
    """Build a metadata dict from a TTS response for logging or storage."""
    return {
        "voice_id": response.voice_id,
        "model_id": response.model_id,
        "content_type": response.content_type,
        "duration_ms": response.duration_ms,
        "character_count": response.character_count,
        "audio_size_bytes": len(response.audio_bytes),
    }


def encode_audio_base64(audio_bytes: bytes) -> str:
    """Encode raw audio bytes as a base64 string for embedding or transport."""
    return base64.b64encode(audio_bytes).decode("utf-8")


def decode_audio_base64(b64_string: str) -> bytes:
    """Decode a base64 audio string back to raw bytes."""
    return base64.b64decode(b64_string)
