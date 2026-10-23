from google.cloud import texttospeech_v1 as tts
from speech_client import get_speech_client
from typing import List, Optional

def list_voices(language_code: Optional[str] = None) -> List[tts.Voice]:
    client = get_speech_client()
    request = tts.ListVoicesRequest(language_code=language_code)
    response = client.list_voices(request=request)
    return response.voices

def select_voice_by_name(voice_name: str) -> Optional[tts.Voice]:
    voices = list_voices()
    for voice in voices:
        if voice.name == voice_name:
            return voice
    return None