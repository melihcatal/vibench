from google.cloud import texttospeech
from typing import List, Dict, Optional

def list_voices(locale: str) -> List[Dict[str, str]]:
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(languages=[locale])
    return [
        {
            "name": voice.name,
            "language_codes": ", ".join(voice.language_codes),
            "ssml_gender": voice.ssml_gender.name if voice.ssml_gender else "NEUTRAL"
        }
        for voice in response.voices
    ]

def select_voice(locale: str, gender: Optional[str] = None) -> Optional[str]:
    voices_list = list_voices(locale)
    if gender:
        matching = [v["name"] for v in voices_list if v["ssml_gender"].lower() == gender.lower()]
        if matching:
            return matching[0]
    if voices_list:
        return voices_list[0]["name"]
    return None
