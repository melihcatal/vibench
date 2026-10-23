from google.cloud import texttospeech
from speech_client import get_text_to_speech_client
from speech_models import VoiceSelection
from typing import List, Dict, Any


def list_voices(language_code: str = None) -> List[Dict[str, Any]]:
    """Lists available voices for a target locale using Google Cloud Text-to-Speech."""
    client = get_text_to_speech_client()
    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_list.append(
            {
                "name": voice.name,
                "language_codes": list(voice.language_codes),
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )
    return voice_list


def select_voice(selection: VoiceSelection) -> Dict[str, Any]:
    """Selects a specific voice for a target locale using Google Cloud Text-to-Speech.
    Returns the details of the selected voice if found, otherwise an empty dict.
    """
    client = get_text_to_speech_client()
    voices = client.list_voices(language_code=selection.language_code).voices

    for voice in voices:
        if selection.name and voice.name == selection.name:
            return {
                "name": voice.name,
                "language_codes": list(voice.language_codes),
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        if not selection.name and selection.ssml_gender:
            if (
                texttospeech.SsmlVoiceGender(voice.ssml_gender).name
                == selection.ssml_gender
            ):
                # Return the first matching voice if no specific name is provided but gender is.
                return {
                    "name": voice.name,
                    "language_codes": list(voice.language_codes),
                    "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
                }
    return {}
