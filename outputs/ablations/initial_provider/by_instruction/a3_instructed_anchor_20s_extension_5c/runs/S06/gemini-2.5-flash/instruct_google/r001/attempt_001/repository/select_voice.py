from typing import Optional, List
from speech_client import TextToSpeechClient
from speech_models import Voice

def list_available_voices(language_code: Optional[str] = None) -> List[Voice]:
    client = TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    return response.voices

def select_voice(language_code: str, ssml_gender: Optional[str] = None, name: Optional[str] = None) -> Optional[Voice]:
    voices = list_available_voices(language_code)
    for voice in voices:
        if (not ssml_gender or voice.ssml_gender == ssml_gender) and \
           (not name or voice.name == name):
            return voice
    return None
