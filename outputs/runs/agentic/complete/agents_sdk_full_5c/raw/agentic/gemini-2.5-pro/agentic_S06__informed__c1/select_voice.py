from typing import List, Optional

from google.cloud import texttospeech

from speech_client import get_speech_client
from speech_models import VoiceDetail


def select_voice(language_code: str) -> Optional[VoiceDetail]:
    """Selects the first available voice for a given language."""
    client = get_speech_client()
    voices = list_voices(language_code)
    if not voices:
        return None
    return voices[0]


def list_voices(language_code: str) -> List[VoiceDetail]:
    """Lists the available voices."""
    client = get_speech_client()
    response = client.list_voices(language_code=language_code)

    voice_details = []
    for voice in response.voices:
        voice_details.append(
            VoiceDetail(
                name=voice.name,
                language_codes=list(voice.language_codes),
                ssml_gender="FEMALE"
                if voice.ssml_gender == texttospeech.SsmlVoiceGender.FEMALE
                else "MALE"
                if voice.ssml_gender == texttospeech.SsmlVoiceGender.MALE
                else "NEUTRAL",
            )
        )
    return voice_details
