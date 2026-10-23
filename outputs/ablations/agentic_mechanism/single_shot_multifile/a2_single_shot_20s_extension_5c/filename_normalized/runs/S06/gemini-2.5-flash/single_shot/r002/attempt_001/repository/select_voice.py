import os
from google.cloud import texttospeech
from typing import List, Dict, Any
from speech_client import get_tts_client

def list_available_voices(language_code: str = None) -> List[Dict[str, Any]]:
    """
    Lists available voices from Google Cloud Text-to-Speech, optionally filtered by language code.
    """
    client = get_tts_client()
    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_list.append({
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz
        })
    return voice_list

def select_voice_by_criteria(
    language_code: str,
    gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.NEUTRAL,
    preferred_name_substring: str = None
) -> Dict[str, Any] | None:
    """
    Selects a voice based on language code, gender, and an optional preferred name substring.
    Returns the first matching voice or None if no match is found.
    """
    available_voices = list_available_voices(language_code=language_code)

    for voice_info in available_voices:
        if voice_info["ssml_gender"] == texttospeech.SsmlVoiceGender(gender).name:
            if preferred_name_substring:
                if preferred_name_substring.lower() in voice_info["name"].lower():
                    return voice_info
            else:
                return voice_info
    return None
