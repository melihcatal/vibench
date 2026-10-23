import os
from google.cloud import texttospeech  # Provider-specific import
from typing import Literal


def generate_audio_preview(
    text: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Standard-A",
    audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"] = "MP3",
) -> bytes:
    """
    Generates spoken previews of translated copy using Google Cloud Text-to-Speech.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice parameters.
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file to return.
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding),
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content  # The audio content as bytes
