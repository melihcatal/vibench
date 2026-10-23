import os
from google.cloud import texttospeech


def list_voices(language_code=None):
    """List available voices for a target locale using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    response = client.list_voices(language_code=language_code)

    voices = []
    for voice in response.voices:
        voice_info = {
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        }
        voices.append(voice_info)

    return voices


def select_voice_for_locale(language_code="en-US", gender="NEUTRAL"):
    """Select a voice for a target locale and gender preference."""
    client = texttospeech.TextToSpeechClient()

    response = client.list_voices(language_code=language_code)

    for voice in response.voices:
        if texttospeech.SsmlVoiceGender(voice.ssml_gender).name == gender:
            return voice.name

    return response.voices[0].name if response.voices else None
