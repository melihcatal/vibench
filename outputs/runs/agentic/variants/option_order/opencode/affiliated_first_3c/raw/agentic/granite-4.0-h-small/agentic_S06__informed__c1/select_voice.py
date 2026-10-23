import os
from speech_client import TextToSpeechClient


def list_voices(language_code: str = None) -> list:
    """List available voices for the configured TTS provider.

    Args:
        language_code (str, optional): ISO language code filter (e.g., 'en-US').

    Returns:
        list: A list of voice descriptors with name, language codes, gender, and custom_id fields.
    """
    client = TextToSpeechClient()
    voices = client.list_voices(language_code=language_code)
    # Return a simplified representation for scripts
    return [
        {
            "name": v.name,
            "language_codes": v.language_codes,
            "gender": v.ssml_gender,
            "custom_id": v.name.split("-")[1],  # Simplified identifier for selection
        }
        for v in voices.voices
    ]


def select_voice(language_code: str, desired_name: str = None) -> str:
    """Select a voice name based on language and optional partial name match.

    Args:
        language_code (str): ISO language code.
        desired_name (str, optional): Partial string to match voice name.

    Returns:
        str: The selected voice's full identifier or raises ValueError.
    """
    voices = list_voices(language_code)
    if not voices:
        raise ValueError(f"No voices found for language: {language_code}")
    if desired_name:
        for v in voices:
            if desired_name.lower() in v["name"].lower():
                return v["name"]
        raise ValueError(f'No voice matching "{desired_name}" found.')
    return voices[0]["name"]  # default to first voice
