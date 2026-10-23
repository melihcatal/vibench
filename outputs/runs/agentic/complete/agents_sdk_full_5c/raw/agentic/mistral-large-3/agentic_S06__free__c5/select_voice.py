from google.cloud import texttospeech_v1
from speech_client import get_speech_client

def list_available_voices(language_code: str = None) -> list:
    """
    Lists available voices for a target locale using Google Cloud Text-to-Speech.
    """
    client = get_speech_client()
    response = client.list_voices(language_code=language_code)
    return [voice.name for voice in response.voices]

def select_voice_by_name(voice_name: str) -> dict:
    """
    Selects a voice by name and returns its details.
    """
    client = get_speech_client()
    response = client.list_voices()
    for voice in response.voices:
        if voice.name == voice_name:
            return {
                "name": voice.name,
                "language_codes": voice.language_codes,
                "ssml_gender": texttospeech_v1.SsmlVoiceGender(voice.ssml_gender).name
            }
    raise ValueError(f"Voice {voice_name} not found.")