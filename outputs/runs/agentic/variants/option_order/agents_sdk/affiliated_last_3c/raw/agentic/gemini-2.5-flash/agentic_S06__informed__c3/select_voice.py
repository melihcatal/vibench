
import os
from typing import List, Dict, Any
from google.cloud import texttospeech
from speech_client import TextToSpeechClient
from speech_models import VoiceSelectionParams

def select_voice(params: VoiceSelectionParams) -> List[Dict[str, Any]]:
    """Lists or selects a voice for a target locale using Google Cloud Text-to-Speech.

    Args:
        params: A VoiceSelectionParams object for filtering voices.

    Returns:
        A list of dictionaries, each representing an available voice.
    """
    client_wrapper = TextToSpeechClient()
    client = client_wrapper.client

    response = client.list_voices(language_code=params.language_code)

    available_voices = []
    for voice in response.voices:
        if params.name and params.name != voice.name:
            continue
        if params.ssml_gender and params.ssml_gender != texttospeech.SsmlVoiceGender(params.ssml_gender.upper()):
            continue

        available_voices.append({
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        })
    return available_voices
