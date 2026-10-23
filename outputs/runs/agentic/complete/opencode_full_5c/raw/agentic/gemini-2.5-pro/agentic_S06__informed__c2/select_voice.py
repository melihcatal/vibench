from speech_client import get_tts_client
from typing import List


def select_voice(language_code: str) -> List[dict]:
    """Lists available voices for a given language code."""
    client = get_tts_client()
    response = client.list_voices(language_code=language_code)

    voices = []
    for voice in response.voices:
        voices.append(
            {
                "name": voice.name,
                "ssml_gender": voice.ssml_gender.name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )
    return voices
