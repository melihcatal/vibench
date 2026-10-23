from google.cloud import texttospeech_v1 as tts
from speech_client import SpeechClient
from speech_models import VoiceInfo, normalize_voice_list
from typing import List, Optional


def list_voices(language_code: Optional[str] = None) -> List[VoiceInfo]:
    client = SpeechClient().get_client()
    response = client.list_voices(language=language_code)
    return normalize_voice_list(response.voices)


def select_voice(language_code: str, ssml_gender: Optional[str] = None) -> VoiceInfo:
    voices = list_voices(language_code)
    for voice in voices:
        if ssml_gender and voice.ssml_gender != ssml_gender:
            continue
        return voice
    raise ValueError(
        f"No matching voice found for language {language_code} and gender {ssml_gender}"
    )
