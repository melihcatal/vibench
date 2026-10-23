from google.cloud import texttospeech_v1 as tts
from speech_client import get_speech_client

def list_voices(language_code: str = None) -> tts.ListVoicesResponse:
    """
    Lists available voices for a target locale using Google Cloud Text-to-Speech.
    """
    client = get_speech_client()
    response = client.list_voices(language_code=language_code)
    return response

def select_voice(language_code: str, voice_name: str = None) -> tts.Voice:
    """
    Selects a voice for a target locale using Google Cloud Text-to-Speech.
    """
    voices = list_voices(language_code)
    for voice in voices.voices:
        if voice_name and voice.name == voice_name:
            return voice
        if not voice_name and language_code in voice.language_codes:
            return voice
    raise ValueError(f"No matching voice found for language_code={language_code} and voice_name={voice_name}")