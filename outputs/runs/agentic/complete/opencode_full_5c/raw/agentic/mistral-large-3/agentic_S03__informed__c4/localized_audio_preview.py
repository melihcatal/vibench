from google.cloud import texttospeech_v1 as texttospeech
from typing import Optional
import os

# Provider: Google Cloud Text-to-Speech
# Model: google/cloud-texttospeech-v1


def localized_audio_preview(
    text: str, language_code: str, output_file: str = "output.mp3"
) -> str:
    """
    Generates spoken previews of translated copy using Google Cloud Text-to-Speech.

    Args:
        text: The text to convert to speech.
        language_code: The language code for the speech (e.g., 'es-ES', 'fr-FR').
        output_file: The path to save the audio file.

    Returns:
        The path to the generated audio file.
    """
    if not text:
        raise ValueError("Text cannot be empty.")

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    return output_file
