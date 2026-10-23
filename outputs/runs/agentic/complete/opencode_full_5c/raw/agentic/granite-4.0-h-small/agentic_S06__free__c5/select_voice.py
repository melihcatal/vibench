# [SAME-SCENARIO] select_voice.py

import os
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()


def list_voices(language_code: str = "en-US") -> list[texttospeech.Voice]:
    """Lists available voices for a language code.

    Args:
        language_code: BCP-47 language tag (e.g., "en-US").

    Returns:
        List of Voice objects.
    """
    return client.list_voices(language=language_code).voices


def get_voice(language_code: str = "en-US", name: str = None) -> texttospeech.Voice:
    """Selects a specific voice from a language code.

    Args:
        language_code: BCP-47 language tag.
        name: Optional voice name (e.g., "en-US-Standard-C"). If omitted,
              returns the default voice for the language.

    Returns:
        The selected Voice object.
    """
    voices = list_voices(language_code)
    if name:
        for v in voices:
            if v.name == name:
                return v
        raise ValueError(f"Voice {name} not found for language {language_code}")
    return voices[0]  # default voice
