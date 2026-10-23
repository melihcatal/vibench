from google.cloud import texttospeech
from typing import List, Dict, Any
import os

def list_voices(language_code: str = None) -> List[Dict[str, Any]]:
    """Lists available voices for a target locale using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_list.append({
            "name": voice.name,
            "language_codes": voice.language_codes,
            "ssml_gender": voice.ssml_gender.name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        })
    return voice_list

