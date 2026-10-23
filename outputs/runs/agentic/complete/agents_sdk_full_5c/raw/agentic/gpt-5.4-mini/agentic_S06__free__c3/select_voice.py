from __future__ import annotations

from typing import List

from google.cloud import texttospeech

from speech_client import get_client
from speech_models import VoiceOption


def select_voice(locale: str) -> List[VoiceOption]:
    client = get_client()
    response = client.list_voices(language_code=locale)
    voices: List[VoiceOption] = []
    for voice in response.voices:
        voices.append(
            VoiceOption(
                name=voice.name,
                language_codes=list(voice.language_codes),
                ssml_gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            )
        )
    return voices
