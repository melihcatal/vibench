import os
import speech_client


def select_voice(locale_code: str = "en-US") -> str:
    """List or select a voice for a target locale using Google Cloud Text-to-Speech.

    Args:
        locale_code (str): Locale code like 'en-US'. Defaults to 'en-US'.

    Returns:
        str: A selected voice name for the locale.
    """
    client = speech_client.TextToSpeechClient()
    voices = client.list_voices(language_code=locale_code)
    # Simplest selection: return the first voice (fallback behavior)
    selected = voices[0].name
    return selected
