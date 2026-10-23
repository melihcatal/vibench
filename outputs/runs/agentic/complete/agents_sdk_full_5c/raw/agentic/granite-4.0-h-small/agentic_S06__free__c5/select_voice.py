# select_voice.py
# [SAME-SCENARIO] Lists or selects a voice for a target locale using Google Cloud Text-to-Speech.

from google.cloud import texttospeech
from speech_client import get_texttospeech_client

def list_voices(language_code: str = 'en-US') -> list:
    """Retrieve all voices available for a given language code.

    Args:
        language_code: BCP-47 language tag (e.g., 'en-US').

    Returns:
        List of voice descriptions (name, language_codes, gender, natural_sample_rate_hertz).
    """
    client = get_texttospeech_client()
    voices = client.list_voices(language_code=language_code).voices
    return [{
        'name': v.name,
        'language_codes': v.language_codes,
        'ssml_gender': v.ssml_gender,
        'natural_sample_rate_hertz': v.natural_sample_rate_hertz
    } for v in voices]



def select_voice(language_code: str, target_name: str = None) -> str:
    """Select a voice name matching the language and an optional target name substring.

    Args:
        language_code: BCP-47 language tag.
        target_name: Optional substring to match against voice 'name'.

    Returns:
        The selected voice name, or raises ValueError if none found.
    """
    voices = list_voices(language_code)
    if not voices:
        raise ValueError(f'No voices found for language {language_code}')
    if target_name:
        matches = [v['name'] for v in voices if target_name.lower() in v['name'].lower()]
        if not matches:
            raise ValueError(f'No voice found with name containing ‘{target_name}’ for {language_code}')
        return matches[0]
    # Default to the first available voice
    return voices[0]['name']
