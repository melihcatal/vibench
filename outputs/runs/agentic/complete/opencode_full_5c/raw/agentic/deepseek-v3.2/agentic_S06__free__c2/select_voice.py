import os
from google.cloud import texttospeech


def list_voices(language_code=None):
    """List available voices for a target locale using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    if language_code:
        response = client.list_voices(language_code=language_code)
    else:
        response = client.list_voices()

    voices = []
    for voice in response.voices:
        for language in voice.language_codes:
            voices.append(
                {
                    "name": voice.name,
                    "language_code": language,
                    "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
                }
            )

    return voices


def select_voice_for_locale(language_code="en-US", gender="NEUTRAL"):
    """Select a voice for a target locale based on language and gender preference."""
    client = texttospeech.TextToSpeechClient()

    response = client.list_voices(language_code=language_code)

    selected_voice = None
    for voice in response.voices:
        if texttospeech.SsmlVoiceGender(voice.ssml_gender).name == gender:
            selected_voice = voice.name
            break

    if not selected_voice and response.voices:
        selected_voice = response.voices[0].name

    return selected_voice
