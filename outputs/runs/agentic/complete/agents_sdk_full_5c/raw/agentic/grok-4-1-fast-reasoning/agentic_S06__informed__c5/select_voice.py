from google.cloud import texttospeech
from speech_client import get_tts_client
from typing import List, Dict, Optional

def list_voices(locale: str = "en-US") -> List[Dict[str, str]]:
    """
    Lists available voices for a target locale using Google Cloud Text-to-Speech.
    """
    client = get_tts_client()
    voices_response = client.list_voices(language_code=locale)
    voices = []
    for voice in voices_response.voices:
        voices.append({
            "name": voice.name,
            "gender": voice.gender.name if voice.gender else "UNSPECIFIED",
            "language_codes": voice.language_codes
        })
    return voices

def select_voice(locale: str, gender: Optional[str] = None, neural: bool = True) -> Optional[str]:
    """
    Selects a suitable voice for the target locale, preferring neural voices.
    """
    voices = list_voices(locale)
    candidates = []
    for v in voices:
        if neural and "Neural2" in v["name"]:
            candidates.append(v["name"])
        elif not neural and "Wavenet" in v["name"]:
            candidates.append(v["name"])
    if gender:
        candidates = [n for n in candidates if gender.lower() in n.lower()]
    return candidates[0] if candidates else (voices[0]["name"] if voices else None)