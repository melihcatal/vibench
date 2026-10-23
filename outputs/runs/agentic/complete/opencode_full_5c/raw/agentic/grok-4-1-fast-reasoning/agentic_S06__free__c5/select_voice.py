from speech_client import get_tts_client
from speech_models import Voice, voice_from_api
from typing import List, Optional


def list_voices(locale: Optional[str] = None) -> List[Voice]:
    client = get_tts_client()
    api_voices = client.voices.get_all()
    voices = [voice_from_api(v) for v in api_voices.voices]
    if locale:
        voices = [
            v
            for v in voices
            if any(l["value"] == locale for l in v.labels if l["category"] == "locale")
        ]
    return voices


def select_voice(locale: str) -> Voice:
    voices = list_voices(locale)
    if not voices:
        raise ValueError(f"No voices available for locale '{locale}'")
    return voices[0]
