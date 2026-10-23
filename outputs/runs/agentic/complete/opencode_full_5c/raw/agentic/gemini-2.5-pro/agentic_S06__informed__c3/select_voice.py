from typing import List
from speech_client import get_speech_client
from speech_models import Voice


def select_voice(language_code: str) -> List[Voice]:
    """Lists the available voices for a specific language."""
    client = get_speech_client()
    voices = client.list_voices(language_code=language_code)

    voice_list = []
    for voice in voices.voices:
        voice_list.append(
            Voice(
                name=voice.name,
                language_code=language_code,
                ssml_gender=voice.ssml_gender.name,
            )
        )
    return voice_list
