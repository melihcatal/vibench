from google.cloud import texttospeech_v1 as tts
from speech_client import get_speech_client
from typing import List, Optional

def list_voices(language_code: Optional[str] = None) -> List[tts.Voice]:
    client = get_speech_client()
    response = client.list_voices(language_code=language_code)
    return response.voices

def select_voice(language_code: str, voice_name: Optional[str] = None) -> tts.Voice:
    voices = list_voices(language_code=language_code)
    if voice_name:
        for voice in voices:
            if voice.name == voice_name:
                return voice
    return voices[0] if voices else None