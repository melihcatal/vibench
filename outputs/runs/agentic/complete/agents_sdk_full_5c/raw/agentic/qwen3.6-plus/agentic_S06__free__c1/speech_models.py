"""
speech_models.py - Define local request, response, and normalization helpers
for Text-to-Speech integrations with ElevenLabs.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from elevenlabs import Voice


@dataclass
class TTSRequest:
    """Normalized request payload for ElevenLabs text-to-speech.

    Attributes:
        text: Plain text to synthesize.
        voice_id: ElevenLabs voice identifier (e.g., '21m00Tcm4TlvDq8ikWAM').
        model_id: ElevenLabs model identifier (e.g., 'eleven_monolingual_v1').
        output_format: Audio format string (e.g., 'mp3_44100_128').
        stability: Voice stability (0.0 - 1.0).
        similarity: Voice similarity boost (0.0 - 1.0).
        style: Style exaggeration (0.0 - 1.0).
        speaker_boost: Enable speaker boost for ElevenLabs models.
        optimize_streaming_latency: Latency optimization level (0-4).
    """
    text: str
    voice_id: str
    model_id: str = "eleven_monolingual_v1"
    output_format: str = "mp3_44100_128"
    stability: float = 0.5
    similarity: float = 0.75
    style: float = 0.0
    speaker_boost: bool = True
    optimize_streaming_latency: int = 0

    def to_elevenlabs_payload(self) -> Dict[str, Any]:
        """Convert to ElevenLabs /v1/text-to-speech API request body."""
        payload: Dict[str, Any] = {
            "model_id": self.model_id,
            "output_format": self.output_format,
            "voice_settings": {
                "stability": self.stability,
                "similarity_boost": self.similarity,
                "style": self.style,
                "use_speaker_boost": self.speaker_boost,
            },
        }
        if self.optimize_streaming_latency:
            payload["optimize_streaming_latency"] = self.optimize_streaming_latency
        return payload


@dataclass
class SSMLRequest(TTSRequest):
    """Normalized request payload for ElevenLabs SSML synthesis.

    Attributes:
        text: SSML-formatted text.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs model supporting SSML.
    """
    text: str = ""
    voice_id: str = ""
    model_id: str = "eleven_multilingual_v2"

    def build_ssml(
        self,
        raw_text: str,
        voice_name: Optional[str] = None,
        pitch: Optional[str] = None,
        rate: Optional[str] = None,
        volume: Optional[str] = None,
        emphasis_level: Optional[str] = None,
        break_duration: Optional[str] = None,
    ) -> str:
        """Construct SSML string with ElevenLabs-compatible prosody controls.

        Args:
            raw_text: The base text to wrap in SSML.
            voice_name: Optional voice name hint (used for logging).
            pitch: Pitch adjustment (e.g., '+10%', '-5%', 'x-high').
            rate: Speaking rate (e.g., '1.2', 'slow', 'fast').
            volume: Volume level (e.g., '+3dB', 'loud', 'soft').
            emphasis_level: Emphasis strength ('strong', 'moderate', 'reduced').
            break_duration: Pause duration (e.g., '500ms', '2s').

        Returns:
            SSML-formatted string.
        """
        parts = ['<speak>']

        if break_duration:
            parts.append(f'<break time="{break_duration}"/>')

        if pitch or rate or volume:
            attrs = []
            if pitch:
                attrs.append(f'pitch="{pitch}"')
            if rate:
                attrs.append(f'rate="{rate}"')
            if volume:
                attrs.append(f'volume="{volume}"')
            attr_str = " ".join(attrs)
            parts.append(f"<prosody {attr_str}>")

        if emphasis_level:
            parts.append(f'<emphasis level="{emphasis_level}">')

        parts.append(raw_text)

        if emphasis_level:
            parts.append("</emphasis>")

        if pitch or rate or volume:
            parts.append("</prosody>")

        if break_duration:
            parts.append(f'<break time="{break_duration}"/>')

        parts.append('</speak>')
        self.text = "\n".join(parts)
        return self.text


@dataclass
class VoiceInfo:
    """Normalized voice information returned from ElevenLabs.

    Attributes:
        voice_id: Unique voice identifier.
        name: Display name of the voice.
        language: Primary language code (e.g., 'en', 'es', 'ja').
        category: Voice category (e.g., 'premade', 'cloned', 'generated').
        description: Optional voice description.
        labels: Additional metadata labels.
        preview_url: URL to a short audio preview.
    """
    voice_id: str
    name: str
    language: str = "en"
    category: str = "premade"
    description: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    preview_url: Optional[str] = None

    @classmethod
    def from_elevenlabs_voice(cls, voice: Voice) -> VoiceInfo:
        """Create VoiceInfo from an ElevenLabs SDK Voice object.

        Args:
            voice: ElevenLabs Voice instance from the SDK.

        Returns:
            Normalized VoiceInfo instance.
        """
        labels = {}
        if voice.labels:
            labels = dict(voice.labels)
        return cls(
            voice_id=voice.voice_id,
            name=voice.name,
            language=labels.get("language", "en"),
            category=voice.category or "premade",
            description=voice.description or "",
            labels=labels,
            preview_url=voice.preview_url if hasattr(voice, 'preview_url') else None,
        )

    def matches_locale(self, target_locale: str) -> bool:
        """Check if this voice matches a target locale code.

        Args:
            target_locale: BCP-47 locale string (e.g., 'en-US', 'es-ES').

        Returns:
            True if the voice's language matches the locale prefix.
        """
        locale_prefix = target_locale.split("-")[0].lower()
        return self.language.lower().startswith(locale_prefix)


@dataclass
class TTSResponse:
    """Normalized response from a text-to-speech synthesis call.

    Attributes:
        audio_bytes: Raw audio byte stream from the provider.
        content_type: MIME type of the audio (e.g., 'audio/mpeg').
        model_id: Model that generated the audio.
        voice_id: Voice used for synthesis.
        character_count: Number of characters billed.
    """
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    model_id: str = ""
    voice_id: str = ""
    character_count: int = 0

    def to_base64(self) -> str:
        """Encode audio bytes as base64 string."""
        return base64.b64encode(self.audio_bytes).decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        """Serialize response metadata (excluding raw audio bytes)."""
        return {
            "content_type": self.content_type,
            "model_id": self.model_id,
            "voice_id": self.voice_id,
            "character_count": self.character_count,
        }


def normalize_voice_list(
    voices: List[Voice],
    target_locale: Optional[str] = None,
    category: Optional[str] = None,
) -> List[VoiceInfo]:
    """Normalize and filter a list of ElevenLabs Voice objects.

    Args:
        voices: List of ElevenLabs Voice objects.
        target_locale: Filter to voices matching this locale (e.g., 'en-US').
        category: Filter to this category (e.g., 'premade').

    Returns:
        Filtered and normalized list of VoiceInfo objects.
    """
    result: List[VoiceInfo] = []
    for voice in voices:
        info = VoiceInfo.from_elevenlabs_voice(voice)
        if target_locale and not info.matches_locale(target_locale):
            continue
        if category and info.category.lower() != category.lower():
            continue
        result.append(info)
    return result


def normalize_speech_text(text: str, max_chars: int = 5000) -> str:
    """Normalize and truncate input text for ElevenLabs synthesis.

    ElevenLabs has character limits per request. This helper ensures
    text is within bounds and has clean whitespace.

    Args:
        text: Raw input text.
        max_chars: Maximum allowed character count.

    Returns:
        Normalized text string.
    """
    normalized = " ".join(text.split())
    if len(normalized) > max_chars:
        normalized = normalized[:max_chars].rsplit(" ", 1)[0]
        normalized = normalized.rstrip(".,;:!?") + "..."
    return normalized
