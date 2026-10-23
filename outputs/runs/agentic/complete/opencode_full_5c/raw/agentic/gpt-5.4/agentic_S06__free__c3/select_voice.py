from __future__ import annotations

from speech_client import get_google_tts_client
from speech_models import VoiceOption, normalize_locale


def list_voices(locale: str) -> list[VoiceOption]:
    client = get_google_tts_client()
    normalized = normalize_locale(locale)
    response = client.list_voices(language_code=normalized)
    return [
        VoiceOption(
            name=voice.name,
            language_codes=list(voice.language_codes),
            gender=voice.ssml_gender.name if voice.ssml_gender is not None else None,
            sample_rate_hertz=voice.natural_sample_rate_hertz,
            provider="google-cloud-texttospeech",
        )
        for voice in response.voices
    ]


def select_voice(
    locale: str, preferred_name_prefix: str | None = None
) -> VoiceOption | None:
    voices = list_voices(locale)
    if preferred_name_prefix:
        for voice in voices:
            if voice.name.startswith(preferred_name_prefix):
                return voice
    return voices[0] if voices else None
