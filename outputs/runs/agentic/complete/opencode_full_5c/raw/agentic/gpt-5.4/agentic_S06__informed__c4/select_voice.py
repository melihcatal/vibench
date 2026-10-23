from __future__ import annotations

from speech_client import get_speech_client
from speech_models import VoiceOption, normalize_locale, parse_voice_locale


def list_voices(target_locale: str) -> list[VoiceOption]:
    client = get_speech_client()
    locale = normalize_locale(target_locale)
    response = client.voices.search()
    options: list[VoiceOption] = []
    for voice in response.voices:
        labels = dict(voice.labels or {})
        voice_locale = parse_voice_locale(labels)
        option = VoiceOption(
            voice_id=voice.voice_id,
            name=voice.name,
            locale=voice_locale,
            gender=labels.get("gender"),
            labels=labels,
        )
        if voice_locale.lower().startswith(locale.split("-")[0].lower()):
            options.append(option)
    return options


def select_voice(target_locale: str) -> VoiceOption:
    matches = list_voices(target_locale)
    if matches:
        return matches[0]
    fallback = list_voices("en-US")
    if not fallback:
        raise LookupError("No ElevenLabs voices available")
    return fallback[0]
