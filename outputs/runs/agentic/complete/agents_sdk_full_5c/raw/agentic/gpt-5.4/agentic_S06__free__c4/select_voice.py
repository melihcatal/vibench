from __future__ import annotations

from typing import List, Optional

from google.cloud import texttospeech

from speech_client import get_google_tts_client
from speech_models import VoiceOption, pick_voice_for_locale


GOOGLE_TTS_PROVIDER = "texttospeech.googleapis.com"


def list_voices(locale: str | None = None) -> List[VoiceOption]:
    client = get_google_tts_client()
    response = client.list_voices(language_code=locale or "")
    return [VoiceOption.from_google_voice(v) for v in response.voices]


def select_voice(locale: str, preferred_name: Optional[str] = None) -> Optional[VoiceOption]:
    voices = list_voices(locale)
    if preferred_name:
        for voice in voices:
            if voice.name == preferred_name:
                return voice
    return pick_voice_for_locale(voices, locale)
