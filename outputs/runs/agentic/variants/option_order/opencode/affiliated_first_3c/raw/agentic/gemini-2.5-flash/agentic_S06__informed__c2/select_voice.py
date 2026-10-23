from speech_client import get_tts_client
from google.cloud import texttospeech
from typing import List, Dict, Any


def list_voices(language_code: str = None) -> List[Dict[str, Any]]:
    """Lists available voices for Google Cloud Text-to-Speech, optionally filtered by language code.

    Args:
        language_code: Optional BCP-47 language code to filter voices, e.g., "en-US".

    Returns:
        A list of dictionaries, each representing an available voice.
    """
    client = get_tts_client()
    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_list.append(
            {
                "language_codes": voice.language_codes,
                "name": voice.name,
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )
    return voice_list


def select_voice(language_code: str, ssml_gender: str = None) -> Dict[str, Any] | None:
    """Selects a voice for a target locale, optionally by gender.

    Args:
        language_code: The BCP-47 language code, e.g., "en-US".
        ssml_gender: Optional SSML voice gender (e.g., "MALE", "FEMALE", "NEUTRAL").

    Returns:
        A dictionary representing the selected voice, or None if no suitable voice is found.
    """
    available_voices = list_voices(language_code)

    for voice in available_voices:
        if ssml_gender:
            if voice["ssml_gender"] == ssml_gender.upper():
                return voice
        else:
            return voice  # Return the first available voice for the language code
    return None
