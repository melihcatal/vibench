import os
from google.cloud import texttospeech


def list_voices(language_code: str = None) -> list:
    """List available voices for a target locale using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    if language_code:
        response = client.list_voices(language_code=language_code)
    else:
        response = client.list_voices()

    voices = []
    for voice in response.voices:
        voices.append(
            {
                "name": voice.name,
                "language_codes": list(voice.language_codes),
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
        )

    return voices


def select_voice(
    language_code: str = "en-US", gender: str = "FEMALE", neural: bool = True
) -> str:
    """Select a voice for a target locale using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    response = client.list_voices(language_code=language_code)

    for voice in response.voices:
        voice_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        is_neural = "Neural" in voice.name

        if voice_gender == gender and neural == is_neural:
            return voice.name

    return response.voices[0].name
