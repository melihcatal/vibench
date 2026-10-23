import os
from google.cloud import texttospeech_v1 as texttospeech
from typing import List, Dict, Any


def retrieval_audio_brief(
    text_to_speak: str, output_filepath: str = "audio_brief.mp3"
) -> str:
    """Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech.

    Args:
        text_to_speak: The text content to be converted to speech.
        output_filepath: The path to save the generated audio file.

    Returns:
        The path to the generated audio file.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_to_speak)

    # Select the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response audio content to the file
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath
