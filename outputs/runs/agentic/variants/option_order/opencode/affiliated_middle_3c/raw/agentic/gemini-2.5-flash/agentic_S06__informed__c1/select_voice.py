import os
from google.cloud import texttospeech
from speech_client import get_text_to_speech_client
from typing import List, Dict, Any


def select_voice(language_code: str = None) -> List[Dict[str, Any]]:
    client = get_text_to_speech_client()
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
