import os
from typing import Optional, List, Dict
from speech_client import get_tts_client

def list_voices(
    language_code: str,
    project_id: Optional[str] = None
) -> List[Dict[str, str]]:
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")
    client = get_tts_client()
    parent = f"projects/{project_id}/locations/global"
    response = client.list_voices(parent=parent, language_code=language_code)
    voices = []
    for voice in response.voices:
        voices.append({
            "name": voice.name,
            "ssml_gender": voice.ssml_gender.name if voice.ssml_gender else "NEUTRAL",
            "language_codes": voice.language_codes,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz
        })
    return voices

def select_voice(
    language_code: str,
    prefer_female: bool = False,
    project_id: Optional[str] = None
) -> str:
    voices = list_voices(language_code, project_id)
    if not voices:
        raise ValueError(f"No voices available for language code {language_code}")
    # Simple selection: first voice
    return voices[0]["name"]
