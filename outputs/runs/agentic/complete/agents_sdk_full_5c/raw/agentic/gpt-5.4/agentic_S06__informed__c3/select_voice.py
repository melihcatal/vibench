from __future__ import annotations

from typing import List, Optional

from speech_client import get_google_tts_client
from speech_models import VoiceOption, normalize_language_code


def list_voices_for_locale(language_code: str) -> List[VoiceOption]:
    client = get_google_tts_client()
    locale = normalize_language_code(language_code)
    response = client.client.list_voices(language_code=locale)
    voices: List[VoiceOption] = []
    for voice in response.voices:
        voices.append(
            VoiceOption(
                name=voice.name,
                language_codes=list(voice.language_codes),
                ssml_gender=getattr(voice.ssml_gender, "name", str(voice.ssml_gender)),
                natural_sample_rate_hz=voice.natural_sample_rate_hertz,
                provider=client.provider,
            )
        )
    return voices


def select_voice(language_code: str, preferred_name_substring: Optional[str] = None) -> Optional[VoiceOption]:
    voices = list_voices_for_locale(language_code)
    if preferred_name_substring:
        needle = preferred_name_substring.lower()
        for voice in voices:
            if needle in voice.name.lower():
                return voice
    return voices[0] if voices else None
