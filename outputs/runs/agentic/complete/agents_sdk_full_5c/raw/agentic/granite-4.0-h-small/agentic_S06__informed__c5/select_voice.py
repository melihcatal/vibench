import os
from speech_client import get_client

def list_voices(locale: str = "en-US") -> list:
    """List available voices for a given locale using Azure Speech TTS.
    Returns a list of dicts with 'Name' and 'DisplayName'.
    """
    client = get_client()
    voices = client.list_voices(language=locale)
    # Expected response contains a list of VoiceInfo objects
    return [{"Name": v.name, "DisplayName": v.display_name} for v in voices]


def select_voice(locale: str = "en-US") -> str:
    """Prompt user or return the first voice for the locale.
    In automated contexts you might select based on naming pattern.
    """
    voices = list_voices(locale)
    if not voices:
        raise RuntimeError("No voices found for locale " + locale)
    # For demonstration, pick the first voice
    return voices[0]["Name"]
