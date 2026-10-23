from typing import List, Optional

from google.cloud import texttospeech

from speech_client import get_speech_client
from speech_models import Voice


def select_voice(language_code: str) -> Optional[Voice]:
    """Lists voices and selects the first available one for a given locale."""
    client = get_speech_client()

    response = client.list_voices(language_code=language_code)
    
    available_voices: List[Voice] = [
        Voice(
            name=voice.name,
            language_codes=list(voice.language_codes),
            ssml_gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
        )
        for voice in response.voices
    ]
    
    if not available_voices:
        return None

    # Return the first standard voice found
    return next((v for v in available_voices if "Standard" in v.name), available_voices[0])
