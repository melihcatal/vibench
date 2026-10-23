from typing import List, Optional
from speech_client import get_speech_client
from speech_models import Voice
from google.cloud.texttospeech_v1.types import SsmlVoiceGender


def list_voices(language_code: str) -> List[Voice]:
    client = get_speech_client()
    response = client.list_voices(language_code=language_code)
    voices = []
    for voice in response.voices:
        voices.append(
            Voice(
                name=voice.name,
                language_codes=list(voice.language_codes),
                ssml_gender=SsmlVoiceGender(voice.ssml_gender).name,
            )
        )
    return voices


def select_voice(
    language_code: str, preferred_name: Optional[str] = None
) -> Optional[Voice]:
    voices = list_voices(language_code)
    if not voices:
        return None

    if preferred_name:
        for voice in voices:
            if voice.name == preferred_name:
                return voice

    return voices[0] if voices else None
