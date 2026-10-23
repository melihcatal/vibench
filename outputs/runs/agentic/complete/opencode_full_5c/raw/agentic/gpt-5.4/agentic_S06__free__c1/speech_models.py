from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SpeechSynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice: str = "alloy"
    model: str = "gpt-4o-mini-tts"
    audio_format: str = "mp3"
    speed: float = 1.0
    locale: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_openai_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "voice": self.voice,
            "format": self.audio_format,
            "speed": self.speed,
        }
        if self.text is not None:
            payload["input"] = self.text
        if self.ssml is not None:
            payload["input"] = self.ssml
            payload["instructions"] = (
                "Render the provided SSML faithfully, including emphasis, pauses, and prosody hints."
            )
        return payload


@dataclass
class SpeechSynthesisResult:
    audio_bytes: bytes
    model: str
    voice: str
    audio_format: str
    provider: str = "openai"


@dataclass
class VoiceOption:
    voice_id: str
    locale: str
    gender: str = "neutral"
    provider: str = "openai"
    preview_text: str = ""


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    model: str
    provider: str = "openai"


@dataclass
class SafetyResult:
    flagged: bool
    categories: Dict[str, bool]
    provider: str = "openai"
    model: str = "omni-moderation-latest"


@dataclass
class EmbeddingResult:
    embedding: List[float]
    model: str
    provider: str = "openai"


@dataclass
class TranscriptResult:
    transcript: str
    model: str
    provider: str = "openai"


OPENAI_VOICE_CATALOG: List[VoiceOption] = [
    VoiceOption(
        voice_id="alloy", locale="en-US", preview_text="Clear general narration voice."
    ),
    VoiceOption(
        voice_id="ash", locale="en-US", preview_text="Grounded and steady delivery."
    ),
    VoiceOption(
        voice_id="ballad", locale="en-GB", preview_text="Warm storytelling cadence."
    ),
    VoiceOption(
        voice_id="coral", locale="en-AU", preview_text="Bright and conversational tone."
    ),
    VoiceOption(
        voice_id="echo", locale="en-US", preview_text="Crisp neutral assistant voice."
    ),
    VoiceOption(
        voice_id="fable", locale="en-GB", preview_text="Expressive long-form narration."
    ),
    VoiceOption(voice_id="nova", locale="en-US", preview_text="Modern polished voice."),
    VoiceOption(
        voice_id="onyx", locale="en-US", preview_text="Lower register announcer style."
    ),
    VoiceOption(
        voice_id="sage", locale="en-US", preview_text="Calm instructional delivery."
    ),
    VoiceOption(
        voice_id="shimmer",
        locale="en-US",
        preview_text="Soft upbeat presentation voice.",
    ),
]


def normalize_locale(locale: str) -> str:
    return locale.replace("_", "-").strip().lower()


def filter_voices_for_locale(locale: str) -> List[VoiceOption]:
    normalized = normalize_locale(locale)
    direct = [
        voice
        for voice in OPENAI_VOICE_CATALOG
        if normalize_locale(voice.locale) == normalized
    ]
    if direct:
        return direct
    language = normalized.split("-")[0]
    return [
        voice
        for voice in OPENAI_VOICE_CATALOG
        if normalize_locale(voice.locale).split("-")[0] == language
    ]
