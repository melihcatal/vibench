from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import google.cloud.texttospeech as tts


@dataclass(frozen=True)
class SpeechConfig:
    project_id: Optional[str] = None
    default_language_code: str = "en-US"
    default_voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT"),
        default_language_code=os.getenv("TTS_DEFAULT_LANGUAGE_CODE", "en-US"),
        default_voice_name=os.getenv("TTS_DEFAULT_VOICE_NAME"),
        speaking_rate=float(os.getenv("TTS_SPEAKING_RATE", "1.0")),
        pitch=float(os.getenv("TTS_PITCH", "0.0")),
    )


def create_client() -> tts.TextToSpeechClient:
    return tts.TextToSpeechClient()


def to_ssml(text: str) -> str:
    text = (text or "").strip()
    if text.startswith("<speak"):
        return text
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f"<speak>{escaped}</speak>"
