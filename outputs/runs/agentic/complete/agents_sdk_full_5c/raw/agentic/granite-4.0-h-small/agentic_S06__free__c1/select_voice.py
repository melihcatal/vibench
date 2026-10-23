import os
import json
from google.cloud import texttospeech
from .speech_client import TextToSpeechClient

def list_voices(language_code: str = 'en-US') -> list:
    """List all available voices for a given language code.

    Returns a list of voice dictionaries with name, language codes, gender, and natural samples.
    """
    client = TextToSpeechClient()
    voices = client.list_voices(language_code=language_code)
    return [
        {
            'name': v.name,
            'language_codes': v.language_codes,
            'gender': v.ssml_gender,
            'natural_sample_rate_hertz': v.natural_sample_rate_hertz
        }
        for v in voices.voices
    ]


def select_voice_by_name(name: str) -> dict:
    """Select a specific voice by its display name.

    Raises ValueError if not found.
    """
    all_voices = list_voices()
    for v in all_voices:
        if v['name'] == name:
            return v
    raise ValueError(f'Voice {name} not found')


def select_default_voice(language_code: str = 'en-US') -> dict:
    """Select the default voice for a language code.
    """
    voices = list_voices(language_code)
    if not voices:
        raise RuntimeError('No voices for language')
    # Simple heuristic: pick first voice that matches gender-neutral criteria
    for v in voices:
        if 'FEMALE' in v['gender'] or 'MALE' in v['gender']:
            continue
        return v
    return voices[0]
