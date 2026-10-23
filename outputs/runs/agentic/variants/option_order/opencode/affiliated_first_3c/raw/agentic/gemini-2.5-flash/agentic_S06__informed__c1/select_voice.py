from google.cloud import texttospeech
from speech_client import TextToSpeechClient
from typing import List, Dict


def list_voices(language_code: str = None) -> List[Dict]:
    """
    Lists available voices for a target locale using Google Cloud Text-to-Speech.
    """
    client = TextToSpeechClient().client
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


def select_voice(language_code: str, ssml_gender: str = None, name: str = None) -> Dict:
    """
    Selects a voice based on criteria. (Simplified for demonstration)
    """
    voices = list_voices(language_code=language_code)

    for voice in voices:
        if name and voice["name"] == name:
            return voice
        if ssml_gender and voice["ssml_gender"] == ssml_gender.upper():
            return voice

    if voices:
        return voices[0]  # Return the first available voice if no specific match
    return {}
