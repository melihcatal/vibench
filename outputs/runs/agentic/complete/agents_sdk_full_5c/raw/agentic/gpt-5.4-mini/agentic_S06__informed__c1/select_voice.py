from __future__ import annotations

from typing import List, Optional

from speech_client import create_client

import google.cloud.texttospeech as tts


def list_voices(language_code: Optional[str] = None) -> List[str]:
    client = create_client()
    response = client.list_voices(language_code=language_code)
    voices = []
    for voice in response.voices:
        voices.append(voice.name)
    return voices


def select_voice(language_code: str, preferred_voice_name: Optional[str] = None) -> str:
    voices = list_voices(language_code)
    if preferred_voice_name and preferred_voice_name in voices:
        return preferred_voice_name
    if voices:
        return voices[0]
    raise ValueError(f"No voices available for locale: {language_code}")
