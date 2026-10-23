# [SAME-SCENARIO] select_voice.py

from typing import List, Optional
from google.cloud import texttospeech
from .speech_client import TextToSpeechClient

def list_all_voices(client: TextToSpeechClient) -> List[str]:
    """Retrieve all available voices from the provider and return a flat list of language tags.

    Returns:
        List of BCP-47 language tags (e.g., 'en-US').
    """
    voices = client.client.list_voices().voices
    return [v.language_codes[0] for v in voices]

def select_voice_for_locale(locale: str, preferred_name: Optional[str] = None) -> str:
    """Select a voice that matches the requested locale. Fallback to provider's default if none matches.

    Args:
        locale: IETF language tag such as 'es-ES'.
        preferred_name: Optional voice identifier to prioritize.
    
    Returns:
        Selected voice name (e.g., 'en-US').
    """
    voices = client.client.list_voices().voices
    for v in voices:
        # language_codes may contain multiple tags; check for matching base language.
        if locale.split('-')[0] in v.language_codes:
            # If a preferred name was supplied, prefer it.
            if preferred_name and v.name == preferred_name:
                return v.name
            # Otherwise return first match.
            return v.name
    # No matching voice found; return default defined in client.
    return client.default_voice
