from typing import List
from speech_client import get_tts_client
from speech_models import Voice


def select_voice(language_code: str) -> List[Voice]:
    client = get_tts_client()
    response = client.list_voices(language_code=language_code)

    voices = []
    for voice in response.voices:
        voices.append(Voice(name=voice.name, language_codes=list(voice.language_codes)))

    return voices
