import os
from google.cloud import texttospeech
from speech_client import get_text_to_speech_client


def list_voices(language_code: str = None):
    """Lists the available voices, optionally filtered by language code."""
    client = get_text_to_speech_client()

    response = client.list_voices(language_code=language_code)
    voices = []
    for voice in response.voices:
        voices.append(
            {
                "name": voice.name,
                "language_codes": voice.language_codes,
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )
    return voices
