from typing import List, Optional
from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import Voice

def list_voices(language_code: Optional[str] = "en-US") -> List[Voice]:
    """Lists the available voices."""
    client = get_tts_client()
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

def select_voice_by_name(name: str, language_code: Optional[str] = "en-US") -> Optional[Voice]:
    """Selects a specific voice by name."""
    all_voices = list_voices(language_code)
    for voice in all_voices:
        if voice.name == name:
            return voice
    return None
