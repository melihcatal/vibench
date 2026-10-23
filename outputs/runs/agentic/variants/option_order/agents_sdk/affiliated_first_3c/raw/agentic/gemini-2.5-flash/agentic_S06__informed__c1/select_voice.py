import os
from google.cloud import texttospeech
from typing import List, Dict, Any
from speech_client import get_text_to_speech_client

def list_voices(language_code: str = "") -> List[Dict[str, Any]]:
    """
    Lists available voices for a given language code using Google Cloud Text-to-Speech.
    If no language_code is provided, lists all supported voices.
    """
    client = get_text_to_speech_client()

    voices = []
    response = client.list_voices(language_code=language_code)
    for voice in response.voices:
        voices.append({
            "name": voice.name,
            "language_codes": voice.language_codes,
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        })
    return voices

def select_voice(language_code: str, preferred_gender: str = None) -> Dict[str, Any]:
    """
    Selects a voice for a target locale, optionally by preferred gender.
    Returns the first matching voice or None if no voice is found.
    """
    available_voices = list_voices(language_code=language_code)

    if preferred_gender:
        for voice in available_voices:
            if voice["ssml_gender"] == preferred_gender.upper():
                return voice
    
    if available_voices:
        return available_voices[0] # Return the first available voice if no specific gender is preferred or found
    
    return None
