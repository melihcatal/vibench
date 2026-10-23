from speech_client import get_tts_client
from typing import List, Dict, Optional


def list_voices(locale: str) -> List[Dict[str, str]]:
    client = get_tts_client()
    voices = client.list_voices(languages=[locale])
    return [
        {
            "name": voice.name,
            "id": voice.name.split("/")[-1],
            "language_codes": ", ".join(voice.language_codes),
            "ssml_gender": voice.ssml_gender.name if voice.ssml_gender else "NEUTRAL",
        }
        for voice in voices.voices
    ]


def select_voice(locale: str, gender: Optional[str] = None) -> str:
    voices = list_voices(locale)
    candidates = voices
    if gender:
        candidates = [v for v in voices if v["ssml_gender"] == gender]
    if candidates:
        return candidates[0]["name"]
    raise ValueError(f"No voice found for locale {locale} with gender {gender}")
