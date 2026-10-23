from typing import List, Optional

from google.cloud import texttospeech

from speech_client import get_speech_client
from speech_models import Voice


def list_voices(language_code: str) -> List[Voice]:
    """Lists available voices for a given language code."""
    client = get_speech_client()
    response = client.list_voices(language_code=language_code)
    
    voices = []
    for voice in response.voices:
        voices.append(
            Voice(
                name=voice.name,
                language_codes=list(voice.language_codes),
                ssml_gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            )
        )
    return voices


def select_voice(language_code: str) -> Optional[Voice]:
    """Selects the first available voice for a given language code."""
    available_voices = list_voices(language_code)
    if not available_voices:
        return None
    return available_voices[0]
