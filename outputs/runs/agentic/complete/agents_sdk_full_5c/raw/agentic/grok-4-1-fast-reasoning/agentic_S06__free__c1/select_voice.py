from speech_client import get_tts_client, get_tts_parent
from typing import List, Dict, Any, Optional

def list_voices(locale: str) -> List[Dict[str, Any]]:
    client = get_tts_client()
    parent = get_tts_parent()
    response = client.list_voices(parent=parent)
    matching_voices = []
    for voice in response.voices:
        if any(locale.lower() in lang_code.lower() for lang_code in voice.language_codes):
            matching_voices.append({
                "name": voice.name.split("/")[-1],
                "language_codes": voice.language_codes,
                "ssml_gender": voice.ssml_gender.name if voice.ssml_gender else None,
                "natural_sample_rate_hertz": getattr(voice, "natural_sample_rate_hertz", None),
            })
    return matching_voices

def select_voice(locale: str, gender: Optional[str] = None) -> str:
    voices = list_voices(locale)
    if gender:
        voices = [v for v in voices if v["ssml_gender"] == gender.upper()]
    if not voices:
        raise ValueError(f"No voice found for locale {locale}" + (f", gender {gender}" if gender else ""))
    # Select first neural/wavenet if possible
    neural_voices = [v for v in voices if "Neural" in v["name"] or "Wavenet" in v["name"]]
    selected = neural_voices[0] if neural_voices else voices[0]
    return selected["name"]
