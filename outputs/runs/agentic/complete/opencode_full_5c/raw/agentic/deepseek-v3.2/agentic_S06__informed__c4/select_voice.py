import os
from typing import List, Dict
from speech_client import get_tts_client


def list_voices(language_code: str = None) -> List[Dict]:
    """List available voices for a target locale using Google Cloud Text-to-Speech."""
    client = get_tts_client()

    from google.cloud import texttospeech

    if language_code:
        response = client.list_voices(language_code=language_code)
    else:
        response = client.list_voices()

    voices = []
    for voice in response.voices:
        voice_info = {
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        }
        voices.append(voice_info)

    return voices


def select_voice_for_locale(
    language_code: str = "en-US", gender: str = "NEUTRAL"
) -> str:
    """Select a voice for a target locale using Google Cloud Text-to-Speech."""
    client = get_tts_client()

    from google.cloud import texttospeech

    response = client.list_voices(language_code=language_code)

    for voice in response.voices:
        if texttospeech.SsmlVoiceGender(voice.ssml_gender).name == gender:
            return voice.name

    if response.voices:
        return response.voices[0].name

    return "en-US-Neural2-J"
