from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import VoiceGender
from typing import List, Optional


def list_voices(language_code: Optional[str] = None) -> List[dict]:
    """Lists available voices for a given language code using Google Cloud Text-to-Speech.

    Args:
        language_code: Optional. The language code to filter voices (e.g., "en-US").

    Returns:
        A list of dictionaries, each representing an available voice.
    """
    client = get_tts_client()
    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_list.append(
            {
                "name": voice.name,
                "language_codes": list(voice.language_codes),
                "ssml_gender": VoiceGender(voice.ssml_gender).name
                if voice.ssml_gender
                else None,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )
    return voice_list


def select_voice(
    language_code: str, ssml_gender: Optional[VoiceGender] = None
) -> Optional[str]:
    """Selects a voice for a target locale and gender using Google Cloud Text-to-Speech.

    Args:
        language_code: The language code for the voice (e.g., "en-US").
        ssml_gender: Optional. The gender of the voice to select.

    Returns:
        The name of the selected voice, or None if no suitable voice is found.
    """
    client = get_tts_client()
    voices = client.list_voices(language_code=language_code).voices

    for voice in voices:
        if ssml_gender is None or (
            voice.ssml_gender and VoiceGender(voice.ssml_gender) == ssml_gender
        ):
            return voice.name
    return None
