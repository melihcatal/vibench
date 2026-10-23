import os
from speech_client import get_text_to_speech_client

def list_voices(locale: str = None):
    """Retrieve available voices for a locale (or all voices if None).
    Returns a list of voice objects with name, locale, gender, and language.
    """
    client = get_text_to_speech_client()
    voices = client.list_voices(language_code=locale).voices
    return voices


def select_voice_by_name(name: str, locale: str = None):
    """Select a single voice by its exact name, optionally narrowing by locale.
    Returns the selected voice object or raises ValueError.
    """
    from typing import List
    all_voices = list_voices(locale)
    for v in all_voices:
        if v.name.lower() == name.lower():
            if locale is None or locale.lower() in v.locale.lower():
                return v
    raise ValueError(f"Voice '{name}' not found for locale {locale}.")