import os
from typing import List
from google.cloud import texttospeech

from embeddings_client import get_text_to_speech_client


def generate_retrieval_audio_brief(
    brief_text: str, output_filepath: str = "audio_brief.mp3"
) -> str:
    """Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech API.

    Args:
        brief_text: The text to convert to speech.
        output_filepath: The path to save the generated audio file.

    Returns:
        The path to the generated audio file.
    """
    client = get_text_to_speech_client()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath
