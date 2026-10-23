from speech_client import get_tts_client
from typing import List, Dict


def select_voice(language_code: str) -> List[Dict]:
    client = get_tts_client()
    voices = client.list_voices(language_code=language_code).voices

    available_voices = []
    for voice in voices:
        available_voices.append(
            {
                "name": voice.name,
                "language_codes": voice.language_codes,
                "ssml_gender": str(voice.ssml_gender).split(".")[-1],
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )
    return available_voices
