from __future__ import annotations

from speech_client import (
    ELEVENLABS_BASE_URL,
    build_elevenlabs_headers,
    normalize_voice_record,
    request_json,
)
from speech_models import VoiceOption, normalize_locale


def list_voices(locale: str | None = None) -> list[VoiceOption]:
    target_locale = normalize_locale(locale)
    response = request_json(
        "GET",
        f"{ELEVENLABS_BASE_URL}/v1/voices",
        headers=build_elevenlabs_headers(),
    )
    options: list[VoiceOption] = []
    for voice in response.get("voices", []):
        normalized = normalize_voice_record(voice)
        option = VoiceOption(provider="elevenlabs", **normalized)
        if target_locale is None or option.locale.lower().startswith(
            target_locale.lower()
        ):
            options.append(option)
    return options


def select_voice(locale: str) -> VoiceOption | None:
    voices = list_voices(locale)
    return voices[0] if voices else None
