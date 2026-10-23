from __future__ import annotations

from typing import List, Optional

from google.cloud import texttospeech

from speech_client import get_client
from speech_models import voice_to_dict


def list_voices(locale: str | None = None) -> List[dict]:
    client = get_client()
    response = client.list_voices(language_code=locale)
    return [voice_to_dict(voice) for voice in response.voices]


def select_voice(locale: str, preferred_name: str | None = None) -> Optional[dict]:
    voices = list_voices(locale)
    if preferred_name:
        for voice in voices:
            if voice.get("name") == preferred_name:
                return voice
    return voices[0] if voices else None
