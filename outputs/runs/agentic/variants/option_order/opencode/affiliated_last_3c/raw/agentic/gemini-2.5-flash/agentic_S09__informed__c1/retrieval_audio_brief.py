import os
from google.cloud import texttospeech
from typing import bytes


def generate_audio_brief(text: str, output_filepath: str = "audio_brief.mp3") -> bytes:
    """
    Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech.
    """
    # Google Cloud Text-to-Speech client will use GOOGLE_APPLICATION_CREDENTIALS
    # environment variable for authentication.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
    return response.audio_content
