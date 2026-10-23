from __future__ import annotations

import os
from typing import List, Optional

from google.cloud import texttospeech

from speech_client import build_client


def list_voices(locale: Optional[str] = None) -> List[str]:
    client = build_client()
    response = client.list_voices(language_code=locale) if locale else client.list_voices()
    return [voice.name for voice in response.voices]


def select_voice(locale: str, preferred_name: Optional[str] = None) -> str:
    voices = list_voices(locale)
    if preferred_name and preferred_name in voices:
        return preferred_name
    if voices:
        return voices[0]
    return locale


if __name__ == "__main__":
    print(select_voice(os.getenv("TTS_LOCALE", "en-US"), os.getenv("TTS_PREFERRED_VOICE")))
