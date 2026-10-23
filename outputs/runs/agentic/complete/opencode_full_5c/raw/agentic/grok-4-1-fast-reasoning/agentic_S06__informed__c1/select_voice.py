from speech_client import get_tts_client
from typing import List


def list_voices_for_locale(language_code: str) -> List[str]:
    client = get_tts_client()
    voices = client.list_voices()
    matching_voices = [
        voice.name for voice in voices.voices if language_code in voice.language_codes
    ]
    return matching_voices


def select_voice(language_code: str, ssml_gender: str = None) -> str:
    voices = list_voices_for_locale(language_code)
    if not voices:
        raise ValueError(f"No voices found for locale {language_code}")
    if ssml_gender:
        for voice_name in voices:
            if ssml_gender.lower() in voice_name.lower():
                return voice_name
    return voices[0]
