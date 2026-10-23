from typing import List, Dict, Optional
from speech_client import get_tts_client


def list_voices(locale: str) -> List[Dict[str, str]]:
    client = get_tts_client()
    voices_response = client.list_voices()
    matching_voices = []
    for voice in voices_response.voices:
        if any(
            locale.lower() in lang_code.lower() for lang_code in voice.language_codes
        ):
            matching_voices.append(
                {
                    "name": voice.name,
                    "language_codes": voice.language_codes,
                    "ssml_gender": voice.ssml_gender.name
                    if voice.ssml_gender
                    else "NEUTRAL",
                }
            )
    return matching_voices


def select_voice(locale: str, gender: Optional[str] = None) -> str:
    voices = list_voices(locale)
    if gender:
        voices = [v for v in voices if gender.lower() in v["ssml_gender"].lower()]
    if not voices:
        raise ValueError(
            f"No suitable voice found for locale '{locale}' and gender '{gender}'"
        )
    return voices[0]["name"]
