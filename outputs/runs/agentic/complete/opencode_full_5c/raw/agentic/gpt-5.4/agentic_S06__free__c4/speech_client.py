from __future__ import annotations

import os
from typing import Iterable

import requests
from openai import OpenAI

from speech_models import VoiceOption, normalize_locale


OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_TRANSCRIPTION_MODEL = os.getenv(
    "OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe"
)
DEEPL_API_URL = os.getenv("DEEPL_API_URL", "https://api.deepl.com/v2/translate")
MODERATION_API_URL = os.getenv(
    "OPENAI_MODERATION_API_URL", "https://api.openai.com/v1/moderations"
)
ELEVENLABS_API_URL = os.getenv("ELEVENLABS_API_URL", "https://api.elevenlabs.io/v1")


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_requests_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "tts-integrations/1.0"})
    return session


def get_elevenlabs_headers() -> dict[str, str]:
    return {
        "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
        "Accept": "application/json",
    }


def default_voice_catalog() -> list[VoiceOption]:
    return [
        VoiceOption(provider="openai", voice_id="alloy", name="Alloy", locale="en-US"),
        VoiceOption(provider="openai", voice_id="ash", name="Ash", locale="en-US"),
        VoiceOption(provider="openai", voice_id="coral", name="Coral", locale="en-US"),
        VoiceOption(provider="openai", voice_id="sage", name="Sage", locale="en-US"),
        VoiceOption(provider="openai", voice_id="verse", name="Verse", locale="en-US"),
    ]


def filter_voices_for_locale(
    voices: Iterable[VoiceOption], locale: str
) -> list[VoiceOption]:
    normalized = normalize_locale(locale)
    language = normalized.split("-", 1)[0]
    return [
        voice
        for voice in voices
        if normalize_locale(voice.locale) == normalized
        or voice.locale.split("-", 1)[0] == language
    ]


def pick_voice_for_locale(
    locale: str, preferred_voice: str | None = None
) -> VoiceOption:
    voices = filter_voices_for_locale(default_voice_catalog(), locale)
    if preferred_voice:
        for voice in voices:
            if voice.voice_id == preferred_voice:
                return voice
    if voices:
        return voices[0]
    return default_voice_catalog()[0]
