import os
from speech_client import get_texttospeech_client

def list_voices(locale: str = None) -> list:
    """Return a list of available voice descriptions for the given locale.
    If locale is None, returns voices for all locales.
    """
    client = get_texttospeech_client()
    voices = client.list_voices(language=locale).get_result()
    return list(voices)


def select_voice(locale: str = None, gender: str = None) -> str:
    """Select a voice identifier that matches the optional locale and gender.
    Returns the first matching voice ID, or raises ValueError if none found.
    """
    candidates = list_voices(locale)
    for v in candidates:
        if gender and v['gender'] != gender.upper():
            continue
        return v['name']
    raise ValueError('No matching voice found')
