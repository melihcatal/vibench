from google.cloud import texttospeech
from typing import List, Dict, Optional


def list_voices(locale: str = "en-US") -> List[Dict]:
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(languages=[locale])
    voices = []
    for voice in response.voices:
        voices.append(
            {
                "name": voice.name,
                "ssml_gender": voice.ssml_gender,
                "language_codes": voice.language_codes,
            }
        )
    return voices


def select_voice(
    locale: str, preferred_gender: Optional[str] = "FEMALE"
) -> Optional[str]:
    voices = list_voices(locale)
    if not voices:
        return None
    if preferred_gender:
        for voice in voices:
            if voice["ssml_gender"] == preferred_gender:
                return voice["name"]
    return voices[0]["name"]
