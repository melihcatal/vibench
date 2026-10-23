from typing import List
import os
from google.cloud import texttospeech_v1


def generate_spoken_previews(texts: List[str], language_code: str) -> List[bytes]:
    """
    Generates spoken previews of translated copy using Google Cloud Text-to-Speech API.
    Uses the Wavenet voice model for high-quality audio.
    """
    client = texttospeech_v1.TextToSpeechClient()

    if not os.getenv("GOOGLE_CLOUD_PROJECT_ID"):
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set")

    audio_contents = []

    for text in texts:
        synthesis_input = texttospeech_v1.SynthesisInput(text=text)
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code=language_code,
            name=f"{language_code}-Wavenet-A",  # Using Wavenet voice model
        )
        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        audio_contents.append(response.audio_content)

    return audio_contents
