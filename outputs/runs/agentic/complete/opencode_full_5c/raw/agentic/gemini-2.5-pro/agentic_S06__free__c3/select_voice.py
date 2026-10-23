from typing import List
from speech_client import get_tts_client
from speech_models import Voice


def select_voice(language_code: str = "en-US") -> List[Voice]:
    """Lists the available voices for a given language code."""
    client = get_tts_client()

    response = client.list_voices(language_code=language_code)

    selected_voices = []
    for voice in response.voices:
        selected_voices.append(
            Voice(
                language_code=language_code,
                name=voice.name,
                ssml_gender=voice.ssml_gender.name,
                natural_sample_rate_hertz=voice.natural_sample_rate_hertz,
            )
        )
    return selected_voices
