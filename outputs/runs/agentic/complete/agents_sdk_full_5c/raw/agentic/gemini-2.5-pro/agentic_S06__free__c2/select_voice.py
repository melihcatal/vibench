from typing import List, Dict

from google.cloud import texttospeech_v1 as texttospeech

from speech_client import get_tts_client
from speech_models import VoiceDetail


def select_voice_by_locale(language_code: str) -> List[VoiceDetail]:
    """
    Lists available voices for a given language code.

    Args:
        language_code: The language code to filter by (e.g., "en-US", "fr-FR").

    Returns:
        A list of VoiceDetail objects matching the locale.
    """
    client = get_tts_client()
    response = client.list_voices(language_code=language_code)
    
    voices = []
    for voice in response.voices:
        voices.append(
            VoiceDetail(
                name=voice.name,
                language_codes=list(voice.language_codes),
                ssml_gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            )
        )
    return voices
