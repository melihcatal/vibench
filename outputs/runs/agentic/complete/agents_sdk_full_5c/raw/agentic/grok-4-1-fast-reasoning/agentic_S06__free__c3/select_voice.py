from google.cloud import texttospeech
from typing import List, Dict, Optional

def list_voices(
    language_code: str = "en-US"
) -> List[Dict[str, str]]:
    """Lists voices for a target locale."""
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code)
    return [
        {
            "name": voice.name,
            "language_codes": ",".join(voice.language_codes),
            "ssml_gender": str(voice.ssml_gender),
        }
        for voice in voices.voices
    ]

def select_voice(
    language_code: str = "en-US",
    ssml_gender: Optional[str] = None
) -> str:
    """Selects a voice for a target locale."""
    voices_list = list_voices(language_code)
    for v in voices_list:
        if ssml_gender is None or v["ssml_gender"] == ssml_gender:
            return v["name"]
    return voices_list[0]["name"] if voices_list else ""
