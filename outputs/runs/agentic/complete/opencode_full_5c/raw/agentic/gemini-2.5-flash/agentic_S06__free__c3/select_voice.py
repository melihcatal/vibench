from google.cloud import texttospeech
from speech_client import get_tts_client
from typing import List, Dict, Any, Optional


def list_voices(language_code: Optional[str] = None) -> List[Dict[str, Any]]:
    client = get_tts_client()

    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_list.append(
            {
                "name": voice.name,
                "language_codes": voice.language_codes,
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )
    return voice_list


def select_voice(
    language_code: str, ssml_gender: Optional[str] = None, name: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    voices = list_voices(language_code=language_code)
    for voice in voices:
        if name and voice["name"] == name:
            return voice
        if ssml_gender and voice["ssml_gender"] == ssml_gender:
            return voice
    return None
