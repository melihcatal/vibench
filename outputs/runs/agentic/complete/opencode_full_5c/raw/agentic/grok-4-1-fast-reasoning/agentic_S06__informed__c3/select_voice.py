from speech_client import get_tts_client
from google.cloud import texttospeech
from typing import List, Dict, Optional


def list_voices(language_code: str) -> List[Dict[str, str]]:
    client = get_tts_client()
    voices_response = client.list_voices(language_code=language_code)
    return [
        {
            "name": voice.name,
            "ssml_gender": voice.ssml_gender.name if voice.ssml_gender else "NEUTRAL",
            "language_codes": ", ".join(voice.language_codes),
        }
        for voice in voices_response.voices
    ]


def select_voice(
    language_code: str, preferred_gender: Optional[str] = None
) -> Optional[str]:
    voices = list_voices(language_code)
    if preferred_gender:
        matching_voices = [
            v for v in voices if v["ssml_gender"] == preferred_gender.upper()
        ]
        if matching_voices:
            return matching_voices[0]["name"]
    if voices:
        return voices[0]["name"]
    return None
