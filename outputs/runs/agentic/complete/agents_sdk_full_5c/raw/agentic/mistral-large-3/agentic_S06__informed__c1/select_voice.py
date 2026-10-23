from typing import List, Dict, Optional
import os
from google.cloud import texttospeech_v1 as texttospeech
from speech_client import get_speech_client

def list_available_voices(
    language_code: Optional[str] = None
) -> List[Dict]:
    """
    List available voices for a target locale using Google Cloud Text-to-Speech.
    """
    client = get_speech_client()
    response = client.list_voices(request={"language_code": language_code} if language_code else {})
    
    voices = []
    for voice in response.voices:
        voices.append({
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz
        })
    
    return voices

def select_voice_by_name(
    voice_name: str
) -> Optional[Dict]:
    """
    Select a voice by name using Google Cloud Text-to-Speech.
    """
    voices = list_available_voices()
    for voice in voices:
        if voice["name"] == voice_name:
            return voice
    return None