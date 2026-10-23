from typing import List
from speech_client import get_speech_client
from speech_models import Voice


def select_voice(language_code: str = "en-US") -> List[Voice]:
    """Lists available voices for a given language code."""
    client = get_speech_client()

    response = client.list_voices(language_code=language_code)

    voices = []
    for voice in response.voices:
        voices.append(
            Voice(
                name=voice.name,
                language_codes=list(voice.language_codes),
                ssml_gender=voice.ssml_gender.name,
                natural_sample_rate_hertz=voice.natural_sample_rate_hertz,
            )
        )
    return voices
