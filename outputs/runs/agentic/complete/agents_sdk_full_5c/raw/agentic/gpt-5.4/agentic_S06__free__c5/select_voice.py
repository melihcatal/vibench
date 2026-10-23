from __future__ import annotations

from typing import List, Optional

from google.cloud import texttospeech

from speech_client import get_texttospeech_client
from speech_models import VoiceOption, filter_voices_for_locale, normalize_locale


def list_voices(locale: Optional[str] = None) -> List[VoiceOption]:
    client = get_texttospeech_client()
    response = client.list_voices(language_code=normalize_locale(locale) if locale else None)
    return [VoiceOption.from_google_voice(voice) for voice in response.voices]


def select_voice_for_locale(locale: str, preferred_name_substring: Optional[str] = "Chirp3") -> VoiceOption:
    voices = filter_voices_for_locale(list_voices(locale), locale)
    if not voices:
        raise LookupError(f"No Google Cloud Text-to-Speech voices found for locale {locale}")
    if preferred_name_substring:
        for voice in voices:
            if preferred_name_substring.lower() in voice.name.lower():
                return voice
    return sorted(voices, key=lambda item: item.name)[0]
