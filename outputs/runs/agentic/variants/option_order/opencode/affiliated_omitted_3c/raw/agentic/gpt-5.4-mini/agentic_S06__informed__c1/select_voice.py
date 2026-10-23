from typing import List, Optional

from google.cloud import texttospeech

from speech_client import build_client


def list_voices(locale: Optional[str] = None) -> List[str]:
    client = build_client()
    response = (
        client.list_voices(language_code=locale) if locale else client.list_voices()
    )
    return [voice.name for voice in response.voices]


def select_voice(locale: str, preferred_name: Optional[str] = None) -> str:
    voices = list_voices(locale)
    if preferred_name and preferred_name in voices:
        return preferred_name
    if voices:
        return voices[0]
    raise ValueError(f"No voices available for locale: {locale}")
