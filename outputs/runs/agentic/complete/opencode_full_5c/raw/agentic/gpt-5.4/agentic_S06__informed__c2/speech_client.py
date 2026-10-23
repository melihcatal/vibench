from __future__ import annotations

import os
from typing import Iterable

from elevenlabs import ElevenLabs

from speech_models import VoiceSelection, normalize_locale


DEFAULT_TTS_MODEL = "eleven_multilingual_v2"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"
DEFAULT_VOICE_ID = os.getenv("ELEVENLABS_DEFAULT_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")


def get_elevenlabs_client() -> ElevenLabs:
    api_key = os.environ["ELEVENLABS_API_KEY"]
    return ElevenLabs(api_key=api_key)


def get_default_voice_id(explicit_voice_id: str | None = None) -> str:
    return explicit_voice_id or DEFAULT_VOICE_ID


def map_voice(voice: object) -> VoiceSelection:
    labels = getattr(voice, "labels", None) or {}
    locale = labels.get("language") or labels.get("accent")
    previews: Iterable[object] = getattr(voice, "preview_urls", None) or []
    preview_url = next(iter(previews), None)
    return VoiceSelection(
        voice_id=getattr(voice, "voice_id"),
        name=getattr(voice, "name"),
        locale=normalize_locale(locale),
        labels=labels,
        preview_url=preview_url,
    )


def list_voices(locale: str | None = None) -> list[VoiceSelection]:
    client = get_elevenlabs_client()
    target_locale = normalize_locale(locale)
    voices = [map_voice(voice) for voice in client.voices.get_all().voices]
    if not target_locale:
        return voices
    return [
        voice
        for voice in voices
        if voice.locale
        and (
            voice.locale == target_locale
            or voice.locale.startswith(target_locale.split("-")[0])
        )
    ]
