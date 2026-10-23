import os

from speech_client import TextToSpeechClient


def list_voices(locale: str = None) -> list:
    """List available voices for a given locale.

    Args:
        locale (str, optional): Locale filter (e.g., 'en-US').

    Returns:
        list: List of voice info dicts (name, gender, language_code).
    """
    client = TextToSpeechClient()
    voices = client.list_voices(locale=locale)
    return voices


def select_voice(locale: str, gender: str = None) -> str:
    """Select a voice based on locale and optional gender preference.

    Args:
        locale (str): Required locale (e.g., 'en-US').
        gender (str, optional): 'MALE', 'FEMALE', or 'NEUTRAL'.

    Returns:
        str: Chosen voice name.
    """
    voices = list_voices(locale)
    # Simple heuristic: pick first matching gender, else first voice
    for voice in voices:
        if gender and voice["gender"] == gender.upper():
            return voice["name"]
    return voices[0]["name"]  # fallback
