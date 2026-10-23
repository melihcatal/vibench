import os
from speech_client import get_tts_client
from typing import List, Dict


def list_voices(language_code: str = None) -> List[Dict]:
    """
    List available voices for a target locale using Google Cloud Text-to-Speech.
    """
    client = get_tts_client()

    try:
        response = client.list_voices(language_code=language_code)
        voices = []

        for voice in response.voices:
            voice_info = {
                "name": voice.name,
                "language_codes": list(voice.language_codes),
                "ssml_gender": voice.ssml_gender.name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
            voices.append(voice_info)

        return voices

    except Exception as e:
        raise Exception(f"Failed to list voices: {str(e)}")


def select_voice_for_locale(
    language_code: str = "en-US", gender: str = "FEMALE"
) -> str:
    """
    Select a voice for a target locale using Google Cloud Text-to-Speech.
    """
    voices = list_voices(language_code)

    if not voices:
        return "en-US-Neural2-J"

    filtered_voices = [
        v
        for v in voices
        if language_code in v["language_codes"] and v["ssml_gender"] == gender
    ]

    if filtered_voices:
        return filtered_voices[0]["name"]

    return voices[0]["name"]
