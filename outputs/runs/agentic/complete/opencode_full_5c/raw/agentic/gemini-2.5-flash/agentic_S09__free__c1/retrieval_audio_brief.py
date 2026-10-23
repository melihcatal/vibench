import os
from typing import List
from google.cloud import (
    texttospeech_v1 as texttospeech,
)  # Google Cloud Text-to-Speech API


def generate_audio_brief(text_brief: str, output_filepath: str) -> str:
    """
    Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech API.
    Saves the audio to the specified output_filepath.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Configure the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The audio content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

    return output_filepath
