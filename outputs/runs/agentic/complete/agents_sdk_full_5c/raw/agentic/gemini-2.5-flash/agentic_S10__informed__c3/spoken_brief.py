import os
from google.cloud import texttospeech_v1 as texttospeech # google-cloud-texttospeech
from typing import Tuple

def generate_spoken_brief(text: str) -> bytes:
    """
    Generates a spoken brief from the model output using Google Cloud Text-to-Speech.
    GOOGLE_APPLICATION_CREDENTIALS handles authentication.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice, e.g., 'en-US-Standard-A' is a concrete voice identifier.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
