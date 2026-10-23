from speech_client import get_tts_client
from google.cloud import texttospeech
from typing import List, Dict, Any


def list_voices(language_code: str = None) -> List[Dict[str, Any]]:
    client = get_tts_client()
    voices = client.list_voices(language_code=language_code).voices

    result = []
    for voice in voices:
        result.append(
            {
                "name": voice.name,
                "language_codes": voice.language_codes,
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )
    return result


def select_voice(
    language_code: str, preferred_gender: str = None, preferred_name_prefix: str = None
) -> Dict[str, Any]:
    voices = list_voices(language_code=language_code)

    if preferred_name_prefix:
        voices = [v for v in voices if v["name"].startswith(preferred_name_prefix)]

    if preferred_gender:
        voices = [v for v in voices if v["ssml_gender"] == preferred_gender.upper()]

    if not voices:
        return {}

    # Simple selection: pick the first one after filtering
    return voices[0]
