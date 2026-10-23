from __future__ import annotations

from typing import List, Optional

from speech_client import get_provider_name, get_tts_client
from speech_models import VoiceOption


def list_voices(locale: str) -> List[VoiceOption]:
    client = get_tts_client()
    response = client.list_voices(language_code=locale)
    options: List[VoiceOption] = []
    for voice in response.voices:
        options.append(
            VoiceOption(
                name=voice.name,
                locale=voice.language_codes[0] if voice.language_codes else locale,
                gender=getattr(voice.ssml_gender, "name", str(voice.ssml_gender)),
                natural_sample_rate_hz=voice.natural_sample_rate_hertz,
                provider=get_provider_name(),
                labels={"google_api": "texttospeech.googleapis.com"},
            )
        )
    return options


def select_voice(locale: str, preferred_name_substring: Optional[str] = None) -> VoiceOption:
    voices = list_voices(locale)
    if not voices:
        raise LookupError(f"No Google Cloud Text-to-Speech voices found for locale {locale}")
    if preferred_name_substring:
        lowered = preferred_name_substring.lower()
        for voice in voices:
            if lowered in voice.name.lower():
                return voice
    return voices[0]
