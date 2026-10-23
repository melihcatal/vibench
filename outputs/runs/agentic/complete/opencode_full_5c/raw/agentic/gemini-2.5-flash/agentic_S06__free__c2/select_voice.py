from typing import List, Dict, Optional
from speech_client import get_tts_client
from speech_models import VoiceSelectionParams


def select_voice(
    language_code: str, name: Optional[str] = None, ssml_gender: Optional[str] = None
) -> List[Dict]:
    """Lists or selects a voice for a target locale using Google Cloud Text-to-Speech."""
    client = get_tts_client()

    response = client.list_voices(language_code=language_code)
    voices = []
    for voice in response.voices:
        if (name is None or voice.name == name) and (
            ssml_gender is None or voice.ssml_gender.name == ssml_gender
        ):
            voices.append(
                {
                    "name": voice.name,
                    "language_codes": voice.language_codes,
                    "ssml_gender": voice.ssml_gender.name,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
                }
            )
    return voices
