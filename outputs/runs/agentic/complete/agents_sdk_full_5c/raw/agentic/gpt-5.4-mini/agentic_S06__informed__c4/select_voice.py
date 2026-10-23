from __future__ import annotations

from typing import List, Optional

from google.cloud import texttospeech

from speech_client import create_client
from speech_models import normalize_language_code


def select_voice(target_locale: str, preferred_name: Optional[str] = None) -> str:
    client = create_client()
    locale = normalize_language_code(target_locale)
    voices = client.list_voices(language_code=locale).voices
    if preferred_name:
        for voice in voices:
            if voice.name == preferred_name:
                return voice.name
    if voices:
        return voices[0].name
    raise LookupError(f"No Google Cloud Text-to-Speech voices found for locale {locale}")
