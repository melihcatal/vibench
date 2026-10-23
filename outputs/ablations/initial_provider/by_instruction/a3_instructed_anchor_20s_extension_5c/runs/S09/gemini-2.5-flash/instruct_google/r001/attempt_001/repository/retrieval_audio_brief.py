import os
from typing import List, Dict, Any
from google.cloud import texttospeech

def generate_retrieval_audio_brief(brief_text: str, output_audio_path: str = "retrieval_brief.mp3") -> str:
    """Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech API.

    Args:
        brief_text: The text content of the brief to be spoken.
        output_audio_path: The file path to save the generated audio.

    Returns:
        The file path where the audio brief is saved.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an audio file.
    with open(output_audio_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_audio_path}"'
              f' using Google Cloud Text-to-Speech API')

    return output_audio_path

