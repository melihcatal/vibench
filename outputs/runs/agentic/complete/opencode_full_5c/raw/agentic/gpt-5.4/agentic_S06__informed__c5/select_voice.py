from __future__ import annotations

from speech_client import DEFAULT_VOICE_ID, get_elevenlabs_client
from speech_models import VoiceOption, normalize_locale


def list_voices(target_locale: str | None = None) -> list[VoiceOption]:
    client = get_elevenlabs_client()
    wanted = normalize_locale(target_locale)
    response = client.voices.search()
    matches: list[VoiceOption] = []
    for voice in response.voices:
        labels = dict(getattr(voice, "labels", {}) or {})
        locale = labels.get("language") or labels.get("locale")
        option = VoiceOption(
            voice_id=voice.voice_id,
            name=voice.name,
            locale=locale,
            labels=labels,
            preview_url=getattr(voice, "preview_url", None),
        )
        if not wanted or normalize_locale(locale) == wanted:
            matches.append(option)
    return matches


def select_voice(target_locale: str) -> VoiceOption:
    voices = list_voices(target_locale)
    if voices:
        return voices[0]
    return VoiceOption(
        voice_id=DEFAULT_VOICE_ID, name="Default ElevenLabs Voice", locale=target_locale
    )
