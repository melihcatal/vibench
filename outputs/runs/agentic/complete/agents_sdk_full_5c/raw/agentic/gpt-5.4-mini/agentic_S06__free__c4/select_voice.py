from __future__ import annotations

from typing import List, Optional

from google.cloud import texttospeech

from speech_client import get_tts_client


def list_voices(language_code: Optional[str] = None) -> List[str]:
    client = get_tts_client()
    response = client.list_voices(language_code=language_code or "")
    voices = []
    for voice in response.voices:
        voices.append(voice.name)
    return voices


def select_voice(language_code: str) -> str:
    voices = list_voices(language_code)
    if voices:
        return voices[0]
    client = get_tts_client()
    response = client.list_voices(language_code="en-US")
    for voice in response.voices:
        if language_code in voice.language_codes:
            return voice.name
    raise ValueError(f"No Google Cloud Text-to-Speech voice available for locale: {language_code}")
