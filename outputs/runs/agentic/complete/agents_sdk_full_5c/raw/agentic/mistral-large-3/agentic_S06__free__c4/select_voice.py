from google.cloud import texttospeech_v1
from speech_client import get_speech_client
from typing import List, Optional


def list_voices(language_code: Optional[str] = None) -> List[texttospeech_v1.Voice]:
    """List available voices for a target locale using Google Cloud Text-to-Speech."""
    client = get_speech_client()
    response = client.list_voices(language_code=language_code)
    return response.voices


def select_voice(language_code: str, voice_name: Optional[str] = None) -> texttospeech_v1.Voice:
    """Select a voice for a target locale using Google Cloud Text-to-Speech."""
    voices = list_voices(language_code)
    
    if voice_name:
        for voice in voices:
            if voice.name == voice_name:
                return voice
        raise ValueError(f"Voice {voice_name} not found for language {language_code}")
    
    return voices[0] if voices else None