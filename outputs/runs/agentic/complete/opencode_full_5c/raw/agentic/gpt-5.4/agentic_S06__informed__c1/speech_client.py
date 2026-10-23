from __future__ import annotations

import os
from typing import Optional

from elevenlabs.client import ElevenLabs


DEFAULT_TTS_MODEL = os.getenv("ELEVENLABS_TTS_MODEL", "eleven_turbo_v2_5")
DEFAULT_OUTPUT_FORMAT = os.getenv("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128")
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")


def get_elevenlabs_api_key() -> str:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise EnvironmentError("ELEVENLABS_API_KEY is required")
    return api_key


def get_tts_client(api_key: Optional[str] = None) -> ElevenLabs:
    return ElevenLabs(api_key=api_key or get_elevenlabs_api_key())


def resolve_voice_id(voice_id: Optional[str] = None) -> str:
    return voice_id or DEFAULT_VOICE_ID


def resolve_output_format(output_format: Optional[str] = None) -> str:
    return output_format or DEFAULT_OUTPUT_FORMAT


def resolve_model_id(model_id: Optional[str] = None) -> str:
    return model_id or DEFAULT_TTS_MODEL
